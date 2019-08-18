class CacheItBaseException(Exception):
    pass


class CacheItValueError(CacheItBaseException, ValueError):
    pass
