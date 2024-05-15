#!/usr/bin/env python3
"""
exercise.py.
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator function to count how many
    times methods of Cache class are called.


    Args:
        method (Callable): The
        method to be decorated.

    Returns:
        Callable: The wrapper function.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment call count.

        Args:
            self: The instance of the class.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Any: Result of the original method.
        """
        self.redis_connection.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator function to store the history
     of inputs and outputs for a particular function.

    Args:
        method (Callable): The method to
        be decorated.

    Returns:
        Callable: The wrapper function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input
        and output history.

        Args:
            self: The instance of the class.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Any: Result of the original method.
        """
        input_data = str(args)
        self.redis_connection.rpush(method.__qualname__ + ":inputs", input_data)
        output_data = str(method(self, *args, **kwargs))
        self.redis_connection.rpush(method.__qualname__ + ":outputs", output_data)
        return output_data

    return wrapper


def replay(fn: Callable):
    """
    Function to display the history of
    calls of a particular function.

    Args:
        fn (Callable): The function to replay.
    """
    r = redis.Redis()
    func_name = fn.__qualname__
    call_count = r.get(func_name)
    try:
        call_count = int(call_count.decode("utf-8"))
    except Exception:
        call_count = 0
    print("{} was called {} times:".format(func_name, call_count))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for input_data, output_data in zip(inputs, outputs):
        try:
            input_data = input_data.decode("utf-8")
        except Exception:
            input_data = ""
        try:
            output_data = output_data.decode("utf-8")
        except Exception:
            output_data = ""
        print("{}(*{}) -> {}".format(func_name, input_data, output_data))


class RedisCache:
    """
    Class to interact with Redis for caching operations.
    """

    def __init__(self):
        """
        Initialize Redis connection and flush the database.
        """
        self.redis_connection = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_connection.flushdb()

    @call_history
    @count_calls
    def store_data(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the
        generated key.

        Args:
            data (Union[str, bytes, int, float]):
             The data to be stored.

        Returns:
            str: The generated key under which
             the data is stored.
        """
        generated_key = str(uuid4())
        self.redis_connection.set(generated_key, data)
        return generated_key

    def retrieve_data(self, key: str,
                      conversion_function: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and optionally convert it.

        Args:
            key (str): The key under which the
             data is stored.
            conversion_function (Optional[Callable], optional):
             A function to convert the retrieved data. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved
             data, optionally converted using the provided function.
        """
        value = self.redis_connection.get(key)
        if conversion_function:
            value = conversion_function(value)
        return value

    def retrieve_string_data(self, key: str) -> str:
        """
        Retrieve data from Redis and convert it to a string.

        Args:
            key (str): The key under which the data is stored.

        Returns:
            str: The retrieved data converted to a string.
        """
        value = self.redis_connection.get(key)
        return value.decode("utf-8")

    def retrieve_integer_data(self, key: str) -> int:
        """
        Retrieve data from Redis and convert it to an integer.

        Args:
            key (str): The key under which the data is stored.

        Returns:
            int: The retrieved data converted to an integer.
        """
        value = self.redis_connection.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
