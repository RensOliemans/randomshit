""" This module plays the game 'dertigen', a dice game. """
import logging
from itertools import product

import begin
from dice import Dice

AMOUNT = 4


def spel(minimum=False):
    """ This method plays the actual game.
    :param minimum: whether to go for the minimum score possible

    :return: (keep, sum(keep)), with keep = the hand that is kept, and
             sum(keep) being the score.
    """
    die = Dice()
    keep = []
    while len(keep) < AMOUNT:
        worp = []
        for _ in range(AMOUNT - len(keep)):
            worp.append(die.roll()[0])
        keep_round = decide_minimum(worp, keep, AMOUNT + 4) if minimum \
            else decide_maximum(worp)
        logging.debug('Throw: %s. to_keep: %s', worp, keep_round)
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


def decide_minimum(dice, chosen=None, goal=10):
    """ The same as decide_maximum(), but then for a minimal score. """
    chosen = chosen or []
    if sum(dice) + sum(chosen) <= goal:
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
    """ What's the chance of throwing <= 10 with 6 dice in 1 try? """
    all_throws = list(product(*[range(1, 7) for _ in range(6)]))
    possible_options = len(all_throws)
    good_options = len([x for x in all_throws if sum(x) <= 10])
    return good_options / possible_options


def kans_boven_30():
    """ What's the chance of throwing > 30 with 6 dice in 1 try? """
    all_throws = list(product(*[range(1, 7) for _ in range(6)]))
    possible_options = len(all_throws)
    good_options = len([x for x in all_throws if sum(x) > 30])
    return good_options / possible_options


@begin.start(auto_convert=True)
@begin.logging
def main(minimum: 'Minimum strategy' = False, runs=1):
    '''Spel'''
    total = 0
    for _ in range(runs):
        hand, score = spel(minimum=minimum)
        logging.info('%s, %s', hand, score)
        total += score
    print('Average: {:.2f}'.format(total / runs))
