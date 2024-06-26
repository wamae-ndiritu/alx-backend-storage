#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
import functools
from typing import Callable, Union


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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs
    and outputs for a particular function.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)
        # Store input parameters
        self._redis.rpush(inputs_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(outputs_key, output)

        return output
    return wrapper


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data inside the redis attribute
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float, None]:
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


def replay(func: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        func (Callable): The function to replay.
    """
    cache = Cache()
    inputs = cache._redis.lrange("{}:inputs".format(func.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(
        func.__qualname__), 0, -1)
    print(f"{func.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{func.__qualname__}{eval(inp.decode())} -> {out.decode()}")
