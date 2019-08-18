import hashlib
import json

from pymemcache.client import base
from pymemcache import serde


class CacheIt:
    def __init__(
            self,
            memcached_host,
            memcached_port,
    ):
        self.memcached_host = memcached_host
        self.memcached_port = memcached_port
        self.requests_count = 0

    @staticmethod
    def _hash_string(input_string):
        sha224 = hashlib.sha224
        return sha224(input_string.encode()).hexdigest()

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
        args_dict = list(args)
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
