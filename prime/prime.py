import time
import begin
import logging
from math import sqrt


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for x in range(5, int(sqrt(n)) + 1, 6):
        if n % x == 0 or n % (x + 2) == 0:
            return False
    return True


@begin.start
@begin.convert(n=int)
@begin.logging
def main(n: 'Number'):
    start = time.time()
    print(is_prime(n))
    logging.info(f'Time taken: {time.time() - start:.5}')
