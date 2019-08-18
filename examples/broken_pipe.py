import time

from cacheit import CacheIt


FAULT = True

do_magic = CacheIt('localhost', 11211)

@do_magic.cacheit_decorator
def get_fibonacci(num):
    if num == 0:
        return 1
    if num == 1:
        return 1

    # simmulate an error
    if num == 80 and FAULT:
        raise Exception

    return get_fibonacci(num-1) + get_fibonacci(num-2)


if __name__ == '__main__':
    start_time = 0
    try:
        sequence = []
        start_time = time.time()
        for i in range(100):
            sequence.append(get_fibonacci(i))
    except Exception:
        print("Error catched!!!")
        print("Time spent on first run: {}".format(time.time() - start_time))
        # let's fix an code issue and rerun this program again
        FAULT = False

        start_time = time.time()
        sequence = []
        for i in range(100):
            sequence.append(get_fibonacci(i))
        print("Time spent on second run: {}".format(time.time() - start_time))

    do_magic._clear_cache()
