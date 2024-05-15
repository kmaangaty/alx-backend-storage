#!/usr/bin/env python3
"""
Module declares a Redis class and methods for caching operations.
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    '''Decorator to count how many times methods of Cache class are called.'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function to increment call count.'''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    '''Decorator to store the history of inputs and outputs for a particular function.'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function to store input and output history.'''
        input_data = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_data)
        output_data = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_data)
        return output_data
    return wrapper

def replay(fn: Callable):
    '''Function to display the history of calls of a particular function.'''
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))

class Cache:
    '''Class that declares a Redis Cache.'''
    def __init__(self):
        '''Initialize Cache instance with Redis connection.'''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Method to store data in Redis and return the generated key.'''
        rkey = str(uuid4())
        self._redis.set(rkey, data)
        return rkey

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''Method to retrieve data from Redis and optionally convert it.'''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''Method to retrieve data from Redis and convert it to string.'''
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        '''Method to retrieve data from Redis and convert it to integer.'''
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
