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


