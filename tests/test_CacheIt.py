import numpy as np
import pandas as pd


from cacheit import CacheIt


def test_hash_string():
    assert CacheIt._hash_string('asd') == 'cda1d665441ef8120c3d3e82610e74ab0d3b043763784676654d8ef1'


def test_get_unique_key():
    instance = CacheIt('localhost', 11211)
    instance._clear_cache()

    @instance.cacheit_decorator
    def some_func(arg1, arg2, kwarg1=1, kwarg2=2):
        return arg1 + arg2 + kwarg1 + kwarg2

    a = some_func(1, 2, kwarg1=-1, kwarg2=-2)
    b = some_func(1, 2, kwarg1=-1, kwarg2=-2)
    assert a == b
    assert instance.requests_count == 1


def test_hash_dataframe():
    df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})
    hash_result = CacheIt._hash_pandas(df)
    assert isinstance(hash_result, str)
    assert hash_result == '41c84b3afe4f6affd02cc4c31030e433a6e9d5b52747f3d7c7e605fb'


def test_hash_series():
    df = pd.Series([1, 2, 3, 4])
    hash_result = CacheIt._hash_pandas(df)
    assert isinstance(hash_result, str)
    assert hash_result == 'bf0f9ed39a15ccb47b3369d31fedc155c571da52f47a311fcff06cc7'


def test_hash_index():
    df = pd.Index([1, 2, 3, 4])
    hash_result = CacheIt._hash_pandas(df)
    assert isinstance(hash_result, str)
    assert hash_result == '8c3496da2b4c2ce381069335b16e9a249c876c33f9729e8ba9abbd81'

    
def test_hash_ndarray():
    array = np.array([1, 2, 3, 4])
    result_hash = CacheIt._hash_ndarray(array)
    assert isinstance(result_hash, str)
    assert result_hash == '46c4f0c1fb94a6327fafea6bb1ddf0dd4ddb09f77142e1afae176f96'
