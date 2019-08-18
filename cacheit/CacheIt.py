import hashlib
import json

from numpy import ndarray
from pymemcache import serde
from pymemcache.client import base

from cacheit.exceptions import CacheItValueError


class CacheIt:
    def __init__(
            self,
            memcached_host,
            memcached_port,
    ):
        self.memcached_host = memcached_host
        self.memcached_port = memcached_port
        self.requests_count = 0
        self.__supported_entity_types__ = (
            ndarray,
            str,
            int,
            float,
        )

    @staticmethod
    def _hash_string(input_string):
        sha224 = hashlib.sha224
        return sha224(input_string.encode()).hexdigest()

    def _hash_ndarray(self, input_array):
        if not isinstance(input_array, ndarray):
            raise CacheItValueError(
                "numpy.ndarray instance was expected but got {}".format(
                    type(input_array)
                )
            )
        string = input_array.data.hex()
        return self._hash_string(string)

    def _hash_object(self, entity):
        """Converting to string non-supported by JSON objects.

        :param entity: object, any item
        :return: object or hash-string
        """
        if not isinstance(entity, self.__supported_entity_types__):
            raise CacheItValueError(
                "Entity is has type {}, while only {} supports".format(
                    type(entity),
                    self.__supported_entity_types__,
                )
            )
        if isinstance(entity, ndarray):
            # getting hash from numpy.ndarray
            return self._hash_ndarray(entity)
        else:
            return entity

    def _clear_cache(self):
        memcached = self._get_connection()
        memcached.flush_all()
        memcached.close()

    def _get_connection(self):
        return base.Client(
            (self.memcached_host, self.memcached_port),
            serializer=serde.python_memcache_serializer,
            deserializer=serde.python_memcache_deserializer,
        )

    def _get_unique_key(self, func, *args, **kwargs):
        func_name = func.__name__
        args_dict = [self._hash_object(x) for x in args]
        args_dict.append(kwargs)
        args_str = json.dumps(args_dict)

        string_to_hash = "{}|{}".format(func_name, args_str)
        resulting_hash = self._hash_string(string_to_hash)
        return resulting_hash

    def cacheit_decorator(self, func, *args, **kwargs):
        def func_wrapper(*args, **kwargs):
            unique_hash = self._get_unique_key(func, *args, **kwargs)
            memcached = self._get_connection()
            cached_value = memcached.get(unique_hash)
            if cached_value is not None:
                self.requests_count += 1
                memcached.close()
                return cached_value

            value_to_cache = func(*args, **kwargs)
            memcached.set(unique_hash, value_to_cache)
            memcached.close()
            return value_to_cache

        return func_wrapper
