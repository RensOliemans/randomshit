from itertools import product

from dice import Dice


def spel():
    hand = list()
    for _ in range(6):
        dice = Dice()
        hand.append(dice)
    worp = []
    for dobbelsteen in hand:
        worp.append(dobbelsteen.rolls(1)[0])


def kans_10_of_lager():
    all_throws = list(product(*[range(1, 7) for _ in range(6)]))
    possible_options = len(all_throws)
    good_options = len([x for x in all_throws if sum(x) <= 10])
    return good_options / possible_options


def kans_boven_30():
    all_throws = list(product(*[range(1, 7) for _ in range(6)]))
    possible_options = len(all_throws)
    good_options = len([x for x in all_throws if sum(x) > 30])
    return good_options / possible_options
