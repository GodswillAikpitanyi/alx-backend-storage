#!/usr/bin/env python3

import redis
import uuid
from typing import Callable, Union
import functools

# Decorator function to count method calls
def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        """Increment the count for the method"""
        self._redis.incr(key)
        """ Call the original method and return its result"""
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    """ Creates a Cache class"""

    def __init__(self):
        """ Initializes the Cache instances"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generates a random key (e.g using uuid), store the input
            data in Redis using the random key method and return the key
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float, None]:
        """Retrieves values from the Redis data Storage"""

        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)
