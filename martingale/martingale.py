import logging
from random import random

import begin
from tqdm import tqdm


def bet(amount, chance):
    # change the chance to improve/decrease the odds
    if random() < chance:
        return (amount * 2, True)
    return (-amount, False)


def start(a: 'Amount' = 1, t: 'Total_money' = 10000, g: 'Goal' = 50000, chance=0.5):
    initial = a
    money = t
    losses = 0
    while money > 0 and money <= g:
        earnings, win = bet(min(a, money), chance)
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
                   g: 'Goal' = 50000, r: 'Rounds' = 1, chance=0.5):
    scores = dict()
    for x in tqdm(range(r)):
        logging.info("\nStarting round number {}.".format(x + 1))
        scores[x + 1] = start(a, t, g, chance)

    logging.debug("\nEnd result:")
    logging.debug(scores.values())
    print("Initial amount: €{:,}. Final amount: €{:,}. Winnings: €{:,}"
          .format(t * r, sum(scores.values()), sum(scores.values()) - t * r))
