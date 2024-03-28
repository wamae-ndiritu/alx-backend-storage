#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Callable, Union


class Cache:
    """
    Class Cache
    """
    def __init__(self):
        """
        Instantiates the objects
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count the number of times a method is called.

        Args:
            method (Callable): The method to be decorated.

        Returns:
            Callable: The decorated method.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data inside the redis attribute
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union
    [str, bytes, int, float, None]:
        """
        Retrieve data from the Redis cache.

        Args:
            key (str): The key under which the data is stored.
            fn (Callable, optional): A function to convert the
            retrieved data to the desired format.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            optionally converted using the provided function.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from the Redis cache
        and convert it to a string.

        Args:
            key (str): The key under which the data is stored.

        Returns:
            Union[str, None]: The retrieved data as a string,
            or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve data from the Redis cache and convert it to an integer.

        Args:
            key (str): The key under which the data is stored.

        Returns:
            Union[int, None]: The retrieved data as an integer,
            or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: int(d))
