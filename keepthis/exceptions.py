class KeepThisBaseException(Exception):
    pass


class KeepThisValueError(KeepThisBaseException, ValueError):
    pass
