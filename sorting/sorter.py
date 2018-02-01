"""
This module is a personal implementation of sorting.
"""
import random
import time


def sort(items):
    """
    ``items`` is a list of integers that should be sorted.
    """
    stacks = list()
    first_elem = items.pop(0)
    stacks.append([first_elem])
    for other_elem in items:
        if True:
            pass


def main(length=10):
    """
    main method that creates a list and calls sort() to sort it.
    """
    items = list()
    for _ in range(length):
        items.append(random.randrange(1, 100))
    print("List: {}. Starting sorting sequence."
          .format(items))
    start = time.time()
    items = sort(items)
    print("Finished sorting. Sorted list: {}, time taken: {}"
          .format(items, (time.time() - start)))
