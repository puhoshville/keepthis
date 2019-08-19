import numpy as np

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


def test_hash_ndarray():
    array = np.array([1, 2, 3, 4])
    result_hash = CacheIt._hash_ndarray(array)
    assert isinstance(result_hash, str)
    assert result_hash == '46c4f0c1fb94a6327fafea6bb1ddf0dd4ddb09f77142e1afae176f96'
