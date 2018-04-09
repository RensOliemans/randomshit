import logging
from itertools import product

import begin
from dice import Dice


def spel(minimum=False):
    die = Dice()
    keep = []
    while len(keep) < 6:
        worp = []
        for _ in range(6 - len(keep)):
            worp.append(die.roll()[0])
        keep_round = decide_minimum(worp, keep) if minimum \
            else decide_maximum(worp)
        logging.debug(worp)
        logging.debug(keep_round)
        logging.debug('\n')
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
    amount = len(dice)
    dice = sorted(dice)
    dice.reverse()
    # all possible throws
    all_throws = list(product(*[range(1, 7) for _ in range(amount)]))
    hand = list()
    for die in dice:
        # higher is the amount of throws where the maximum die is higher
        # than the current die
        higher = len([x for x in all_throws if max(x) > die])
        # so, we have:
        #   all_throws:  all possible throws with the amount of dice left
        #   higher:      the throws possible with a higher maximum die (so
        #                  'better' throws if you want to throw high)
        #   all_throws - higher:
        #                the throws which don't have a higher die in it
        # so, append the die to the hand if there are less throws left with
        # a 'better' option than the rest of the throws
        if higher < len(all_throws) - higher:
            hand.append(die)
            amount -= 1
            all_throws = list(product(*[range(1, 7) for _ in range(amount)]))
    return hand or [max(dice)]


def decide_minimum(dice, chosen=None):
    chosen = chosen or []
    if sum(dice) + sum(chosen) <= 10:
        return dice

    amount = len(dice)
    dice = sorted(dice)
    dice.reverse()
    all_throws = list(product(*[range(1, 7) for _ in range(amount)]))
    hand = list()
    for die in dice:
        # lower is the amount of throws where the minimum die is lower
        # than the current die
        lower = len([x for x in all_throws if min(x) < die])
        if lower < len(all_throws) - lower:
            hand.append(die)
            amount -= 1
            all_throws = list(product(*[range(1, 7) for _ in range(amount)]))
    return hand or [min(dice)]


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


@begin.start(auto_convert=True)
@begin.logging
def main(minimum: 'Minimum strategy' = False):
    '''Spel'''
    print(spel(minimum=minimum))
