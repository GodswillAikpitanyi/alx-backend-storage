#!/usr/bin/env python3

import redis
import uuid
from typing import Union


class Cache:
    """ Creates a Cache class"""

    def __init__(self):
        """ Initializes the Cache instances"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generates a random key (e.g using uuid), store the input
            data in Redis using the random key method and return the key
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
