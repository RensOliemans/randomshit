from dice import Dice
from scipy.special import comb
from itertools import permutations


def spel():
    hand = list()
    for _ in range(6):
        d = Dice()
        hand.append(d)
    worp = []
    for dobbelsteen in hand:
        worp.append(dobbelsteen.rolls(1)[0])


def kans_10_of_lager():
    return (  # 1 1 1 1 1 1
            (1/6)**6 +
            # 1 1 1 1 1 (2 / 3 / 4)
            (1/6)**5 * (3/6) * comb(6, 1) +
            # 1 1 1 1 (2 2 / 2 3 / 3 2 / 3 3)
            (1/6)**4 * (2/6)**2 * comb(6, 2) +
            # 1 1 1 (2 2 2)
            (1/6)**3 * (1/6)**3 * comb(6, 3) +
            # 1 1 1 (223 / 232 / 322)
            (1/6)**3 * (1/6)**3 * comb(3, 1) +
            # 1 1 2 2 2 2
            (1/6)**4 * (1/6)**6 * comb(6, 4))


def kans_boven_30():
    all_throws = list(permutations(range(7), 6))
    possible_options = len(all_throws)
    good_options = len([x for x in all_throws if sum(x) > 30])
    return good_options / possible_options
