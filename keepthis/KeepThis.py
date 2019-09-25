import hashlib
import json

import numpy as np
import pandas as pd
from pymemcache import serde
from pymemcache.client import base

from keepthis.MemcachedConnection import MemcachedConnection
from keepthis.exceptions import KeepThisValueError


class KeepThis:
    def __init__(
            self,
            memcached_host,
            memcached_port,
    ):
        self.memcached_host = memcached_host
        self.memcached_port = memcached_port
        self.__supported_entity_types__ = (
            np.ndarray,
            str,
            int,
            float,
        )

    @staticmethod
    def _hash_string(input_string):
        sha224 = hashlib.sha224
        return sha224(input_string.encode()).hexdigest()

    @staticmethod
    def _hash_ndarray(input_array):
        if not isinstance(input_array, np.ndarray):
            raise KeepThisValueError(
                "numpy.ndarray instance was expected but got {}".format(
                    type(input_array)
                )
            )
        string = input_array.data.hex()
        return KeepThis._hash_string(string)

    @staticmethod
    def _hash_pandas(input_dataframe):
        if not isinstance(input_dataframe, (pd.DataFrame, pd.Series, pd.Index)):
            raise KeepThisValueError(
                "numpy.ndarray instance was expected but got {}".format(
                    type(input_dataframe)
                )
            )
        string = pd.util.hash_pandas_object(input_dataframe).values.data.hex()
        return KeepThis._hash_string(string)

    def _hash_object(self, entity):
        """Converting to string non-supported by JSON objects.

        :param entity: object, any item
        :return: object or hash-string
        """
        if not isinstance(entity, self.__supported_entity_types__):
            raise KeepThisValueError(
                "Entity is has type {}, while only {} supports".format(
                    type(entity),
                    self.__supported_entity_types__,
                )
            )
        if isinstance(entity, np.ndarray):
            # getting hash from numpy.ndarray
            return self._hash_ndarray(entity)
        elif isinstance(entity, (pd.DataFrame, pd.Series, pd.Index)):
            # getting hash from pandas.DataFrame
            return self._hash_pandas(entity)
        else:
            return entity

    def drop(self):
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

    def this(self, func, *args, **kwargs):
        def func_wrapper(*args, **kwargs):
            unique_hash = self._get_unique_key(func, *args, **kwargs)
            with MemcachedConnection(self.memcached_host, self.memcached_port) as memcached:
                cached_value = memcached.get(unique_hash)
                if cached_value is not None:
                    memcached.close()
                    return cached_value

                value_to_cache = func(*args, **kwargs)
                memcached.set(unique_hash, value_to_cache)

            return value_to_cache

        return func_wrapper
