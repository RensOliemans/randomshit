from itertools import product

from dice import Dice


def spel():
    die = Dice()
    keep = []
    while len(keep) < 6:
        worp = []
        for _ in range(6 - len(keep)):
            worp.append(die.roll()[0])
        keep_round = decide_maximum(worp)
        keep += keep_round
    return (keep, sum(keep))


def decide_maximum(dice):
    """
    The basic idea of the algorithm:
      You have a certain amount of dice left. To goal is to decide when to
      'settle' for a lower throw - for example, in the first throw, you might
      decide that a 5 is too low to keep (you might have a decent chance to
      throw higher than that), but at the end a 5 is enough (there is a higher
      chance of throwing lower than a 5 than >= 5).
    """
    all_throws = list(product(*[range(1, 7) for _ in range(len(dice))]))
    hand = list()
    for die in dice:
        higher = len([x for x in all_throws if max(x) > die])
        if higher < len(all_throws) - higher:
            hand.append(die)
    return hand or [max(dice)]


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
