#!/usr/bin/env python3

import redis
import uuid
from typing import Callable, Union
import functools

# task 2
""" Decorator function to count method calls"""
def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        """Increment the count for the method"""
        self._redis.incr(key)
        """ Call the original method and return its result"""
        return method(self, *args, **kwargs)
    return wrapper

# task 3
""" Decorator function to store the history of inputs and outputs """
def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        """ store the input arguments as a string in Redis """
        input_str = str(args)
        self._redis.rpush(input_key, input_str)

        """ Call the original method and retrieve the output """
        output = method(self, *args, **kwargs)

        """ Store the output as a string in Redis """
        output_str = str(output)
        self._redis.rpush(output_key, output_str)

        return output
    return wrapper

# task 0
class Cache:
    """ Creates a Cache class"""

    def __init__(self):
        """ Initializes the Cache instances"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generates a random key (e.g using uuid), store the input
            data in Redis using the random key method and return the key
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(func: Callable):
        """ Get the qualified name of the function """
        func_name = func.__qualname__

        """ Get the input and output keys """
        input_key = func_name + ":inputs"
        output_key = func_name + ":outputs"

        """ Retrieve the input and output history from Redis """
        input_history = cache._redis.lrange(input_key, 0, -1)
        output_history = cache._redis.lrange(output_key, 0, -1)

        """ Display the history of calls """
        print(f"{func_name} was called {len(input_history)} times:")

        for inputs, output in zip(input_history, output_history):
             # Convert bytes to string
            input_str = inputs.decode('utf-8')
             # Convert bytes to string
            output_str = output.decode('utf-8')
            print(f"{func_name}(*{input_str}) -> {output_str}")


# task 1
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
