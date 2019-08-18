import time

from cacheit import CacheIt

# provide connection parameters to memcached
# DO NOT PROVIDE PRODUCTION PARAMETERS! WE WILL FLUSH RESULT in the end! =)
do_magick = CacheIt('localhost', 11211)


@do_magick.cacheit_decorator
def some_long_calculations(arg1, arg2, kwarg=100):
    """Implement some long to wait calculations"""
    time.sleep(3)
    return arg1 + arg2 + kwarg


if __name__ == '__main__':
    # do some calculations by your self
    print("Okay, it's time to work! Let's run my calculations!")
    time_start = time.time()
    result = some_long_calculations(1, 2, kwarg=40)
    print("My result: {}\nTime spent: {}".format(result, time.time() - time_start))

    print("Share same code with your teammate, and you will be inspired that he will reproduce results much faster!")
    time_start = time.time()
    result = some_long_calculations(1, 2, kwarg=40)
    print("Teammate got result: {}\nTime spent: {}".format(result, time.time() - time_start))


    do_magick._clear_cache()
