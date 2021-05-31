import time
from typing import List
from multiprocessing import Pool

from game import Game, DirtyA, Other, Person, Vicky

X = 300
C = 38
N = 10000


def run():
    # analyze('verspreid', verspreid)
    analyze('verdeeld_een_uur', verdeeld_een_uur)
    analyze('verdeeld_twee_uur', verdeeld_twee_uur, factor=2)
    analyze('random_in_uur', random_in_uur)
    analyze('vicky', vicky)


def analyze(name, f, factor=1):
    p = Pool(8)
    start = time.time()
    results = p.starmap(f, [[X, C]] * N)
    wins = len([s for s in results if s]) * factor
    print(f'Win % for {name}: {wins / N:.2%}')
    print(f'Took {time.time() - start:.2f}s')
    p.close()


def verspreid(x=X, c=C):
    for hour in range(c):
        others: List[Person] = [Other() for _ in range(x)]
        us = DirtyA()
        total = others + [us]
        game = Game(total)
        if game.roll() is us:
            return True
    return False


def random_in_uur(x=X, c=C):
    others: List[Person] = [Other() for _ in range(x)]
    us = [DirtyA() for _ in range(c)]
    total = others + us
    game = Game(total)
    return game.roll() in us


def vicky(x=X, c=C):
    others: List[Person] = [Other() for _ in range(x)]
    us = [Vicky() for _ in range(c)]
    total = others + us
    game = Game(total)
    return game.roll() in us


def verdeeld(x=X, c=C, total=60):
    others: List[Person] = [Other() for _ in range(x)]
    us = [DirtyA() for _ in range(c)]
    for i, person in enumerate(us):
        person.guess = i * (total / 37)
    total = others + us
    game = Game(total)
    return game.roll() in us


def verdeeld_een_uur(x=X, c=C):
    return verdeeld(x, c, 60)


def verdeeld_twee_uur(x=X, c=C):
    return verdeeld(x, c, 120)





if __name__ == '__main__':
    run()
