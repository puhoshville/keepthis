import unittest.mock as mock

import numpy as np
import pandas as pd
from pymemcache.test.utils import MockMemcacheClient

from keepthis import KeepThis


class CustomMockMemcacheClient(MockMemcacheClient):
    def close(self):
        pass


def test_hash_string():
    assert KeepThis._hash_string('asd') == 'cda1d665441ef8120c3d3e82610e74ab0d3b043763784676654d8ef1'


@mock.patch('pymemcache.client.base.Client', new=CustomMockMemcacheClient)
def test_get_unique_key():
    keep = KeepThis('localhost', 11211)

    @keep.this
    def some_func(arg1, arg2, kwarg1=1, kwarg2=2):
        return arg1 + arg2 + kwarg1 + kwarg2

    a = some_func(1, 2, kwarg1=-1, kwarg2=-2)
    b = some_func(1, 2, kwarg1=-1, kwarg2=-2)
    assert a == b


def test_hash_dataframe():
    df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})
    hash_result = KeepThis._hash_pandas(df)
    assert isinstance(hash_result, str)
    assert hash_result == '41c84b3afe4f6affd02cc4c31030e433a6e9d5b52747f3d7c7e605fb'


def test_hash_series():
    df = pd.Series([1, 2, 3, 4])
    hash_result = KeepThis._hash_pandas(df)
    assert isinstance(hash_result, str)
    assert hash_result == 'bf0f9ed39a15ccb47b3369d31fedc155c571da52f47a311fcff06cc7'


def test_hash_index():
    df = pd.Index([1, 2, 3, 4])
    hash_result = KeepThis._hash_pandas(df)
    assert isinstance(hash_result, str)
    assert hash_result == '8c3496da2b4c2ce381069335b16e9a249c876c33f9729e8ba9abbd81'


def test_hash_ndarray():
    array = np.array([1, 2, 3, 4], np.int64)
    result_hash = KeepThis._hash_ndarray(array)
    assert isinstance(result_hash, str)
    assert result_hash == '46c4f0c1fb94a6327fafea6bb1ddf0dd4ddb09f77142e1afae176f96'
