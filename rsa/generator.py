from random import randrange, getrandbits
from itertools import repeat
from string import digits
import numpy as np
from math import sqrt

numbers = list()


def generate(n):
    def isProbablePrime(n, t=7):
        def isComposite(a):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2 ** i * d, n) == n - 1:
                    return False
            return True

        assert n > 0
        if n < 3:
            return [False, False, True][n]
        elif not n & 1:
            return False
        else:
            s, d = 0, n - 1
            while not d & 1:
                s += 1
                d >>= 1
        for _ in repeat(None, t):
            if isComposite(randrange(2, n)):
                return False
        return True
    p = getrandbits(n)
    while not isProbablePrime(p):
        p = getrandbits(n)
    return p


def crack(product, length1=None, length2=None):
    length = len(str(product))
    even = length % 2 == 0
    length1 = length1 or (length // 2)
    length2 = length2 or (length // 2) if even else (length // 2) + 1
    found_primes_1 = list()
    found_primes_2 = list()
    found = False
    while not found:
        (find_prime_1, found_primes_1) = find_prime(length1, found_primes_1)
        (find_prime_2, found_primes_2) = find_prime(length2, found_primes_2)
        found = find_prime_1 * find_prime_2 == product


def find_prime(length, found_primes=[]):
    start = found_primes[-1] + 1 if found_primes else 10**(length - 1)
    end = 10**(length) - 1
    for x in range(start, end):
        if is_prime(x):
            found_primes.append(x)
            return (x, found_primes)


def main():
    print("This program will generate secure random numbers of a given length")
    amount = int(input("How many numbers? "))
    for _ in range(amount):
        length = int(input("How many bits? "))
        numbers.append(generate(length))
    prod = np.product(numbers)
    print("Numbers: {}, Product: {}".format(numbers, prod))
    print("Starting to crack..")
    crack(prod)


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


if __name__ == "__main__":
    main()
