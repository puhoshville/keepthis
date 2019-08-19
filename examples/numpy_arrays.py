import time

import numpy as np

from keepthis import KeepThis

keep = KeepThis('localhost', 11211)


@keep.this
def sum_of_squares(array):
    time.sleep(5)
    return np.sum(np.power(array, 10))


if __name__ == '__main__':
    asd = np.random.rand(1000)
    start_time = time.time()
    sum_of_squares(asd)
    print("First run in {} seconds".format(time.time()-start_time))

    start_time = time.time()
    sum_of_squares(asd)
    print("Second run in {} seconds".format(time.time() - start_time))

    keep.drop()
