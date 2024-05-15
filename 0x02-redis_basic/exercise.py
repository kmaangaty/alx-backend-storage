#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
import functools
from typing import Union

def count_calls(method):
    """
    Decorator to count method calls
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment call count
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method):
    """
    Decorator to store input and output history
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input and output history
        """
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        input_data = str(args)
        self._redis.rpush(inputs_key, input_data)
        output_data = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output_data)
        return output_data
    return wrapper

class Cache:
    """
    Cache class to interact with Redis for storing and retrieving data
    """
    def __init__(self) -> None:
        """
        Initialize Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the generated key

        Parameters:
            data (Union[str, bytes, int, float]): The data to be stored in Redis

        Returns:
            str: The generated key under which the data is stored in Redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn=None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and convert it using fn if provided

        Parameters:
            key (str): The key under which the data is stored in Redis
            fn (callable, optional): A function to convert the retrieved data. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved data, optionally converted using fn
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data


    def get_str(self, key: str) -> str:
        """
        Retrieve data from Redis and convert it to string

        Parameters:
            key (str): The key under which the data is stored in Redis

        Returns:
            str: The retrieved data converted to string
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve data from Redis and convert it to integer

        Parameters:
            key (str): The key under which the data is stored in Redis

        Returns:
            int: The retrieved data converted to integer
        """
        return self.get(key, fn=int)
