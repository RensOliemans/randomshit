import time
from typing import List
from multiprocessing import Pool

from game import Game, DirtyA, Other, Person


X = 300
C = 38
N = 40000


def run():
    p = Pool(8)
    start = time.time()
    s1s = p.starmap(s1, [[X, C]] * N)
    print(f'Win % for s1: {len([s for s in s1s if s]) / N:.2%}')
    print(f'Took {time.time() - start:.2f}s')

    start = time.time()
    s2s = p.starmap(s2, [[X, C]] * N)
    print(f'Win % for s2: {len([s for s in s2s if s]) / N:.2%}')
    print(f'Took {time.time() - start:.2f}s')


def s1(x=X, c=C):
    for hour in range(c):
        others: List[Person] = [Other() for _ in range(x)]
        us = DirtyA()
        total = others + [us]
        game = Game(total)
        if game.roll() is us:
            return True
    return False


def s2(x=X, c=C):
    others: List[Person] = [Other() for _ in range(x)]
    us = [DirtyA() for _ in range(c)]
    total = others + us
    game = Game(total)
    return game.roll() in us


if __name__ == '__main__':
    run()
