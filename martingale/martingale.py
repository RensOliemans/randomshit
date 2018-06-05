import logging
from random import random

import begin


def bet(amount):
    # change the chance to improve/decrease the odds
    chance = 0.5
    if random() < chance:
        return (amount * 2, True)
    return (-amount, False)


# @begin.start(auto_convert=True)
def start(a: 'Amount' = 1, t: 'Total_money' = 10000, g: 'Goal' = 50000):
    initial = a
    money = t
    losses = 0
    while money > 0 and money <= g:
        earnings, win = bet(min(a, money))
        money += earnings

        if win:
            losses = 0
            a = initial
        else:
            # just lost, double betting amount
            losses += 1
            a *= 2
            if losses > 12:
                logging.info("{} losses in a row, betting amount: €{:,}"
                             .format(losses, a))
                logging.info("Currently have €{:,}".format(money))
    logging.info("Finished, money is €{:,}.".format(money))
    return money


@begin.start(auto_convert=True)
@begin.logging
def multiple_tries(a: 'Amount' = 1, t: 'Total_money' = 10000,
                   g: 'Goal' = 50000, r: 'Rounds' = 1):
    scores = dict()
    for x in range(r):
        logging.info("\nStarting round number {}.".format(x + 1))
        scores[x + 1] = start(a, t, g)

    logging.debug("\nEnd result:")
    logging.debug(scores.values())
    print("Initial amount: €{:,}. Final amount: €{:,}. Winnings: €{:,}"
          .format(t * r, sum(scores.values()), sum(scores.values()) - t * r))
