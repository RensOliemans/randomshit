import time
from math import sqrt


def is_prime(n):
    start = time.time()
    if n <= 1:
        print("Time taken: " + str(time.time() - start))
        return False
    if n <= 3:
        print("Time taken: " + str(time.time() - start))
        return True
    if n % 2 == 0 or n % 3 == 0:
        print("Time taken: " + str(time.time() - start))
        return False
    for x in range(5, int(sqrt(n)) + 1, 6):
        if n % x == 0 or n % (x + 2) == 0:
            print("Time taken: " + str(time.time() - start))
            return False
    print("Time taken: " + str(time.time() - start))
    return True
