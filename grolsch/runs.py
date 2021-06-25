import time
from typing import List
from multiprocessing import Pool

from game import Game, DirtyA, Other, Person, Vicky

X = 38
C = 38
N = 10000


def run():
    analyze('verdeeld2', verdeeld2)
    analyze('verdeeld_een_uur', verdeeld_een_uur)
    analyze('verdeeld_twee_uur', verdeeld_twee_uur, factor=2)
    analyze('verdeeld_acht_uur', verdeeld_acht_uur, factor=8)
    analyze('verdeeld_dag_uur', verdeeld_dag, factor=24)
    analyze('verdeeld_37_uur', verdeeld_37, factor=37)
    analyze('random_in_uur', random_in_uur)
    analyze('vicky', vicky)
    analyze('verspreid', verspreid)


def analyze(name, f, factor=1):
    p = Pool(8)
    start = time.time()
    results = p.starmap(f, [[X, C]] * N)
    wins = len([s for s in results if s]) * factor
    chance = wins / N
    chance = 1 - (1 - chance) ** factor
    print(f'Win % for {name}: {chance:.2%}')
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


def verdeeld2(x=X, c=C):
    others: List[Person] = [Other() for _ in range(x)]
    us = [DirtyA() for _ in range(c)]
    for i, person in enumerate(us):
        person.guess = i * (60 / 5)
    total = others + us
    game = Game(total)
    return game.roll() in us


def verdeeld_een_uur(x=X, c=C):
    return verdeeld(x, c, 60)


def verdeeld_twee_uur(x=X, c=C):
    return verdeeld(x, c, 120)


def verdeeld_acht_uur(x=X, c=C):
    return verdeeld(x, c, 60 * 8)


def verdeeld_dag(x=X, c=C):
    return verdeeld(x, c, 60 * 24)


def verdeeld_37(x=X, c=C):
    return verdeeld(x, c, 60 * 37)


if __name__ == '__main__':
    run()
