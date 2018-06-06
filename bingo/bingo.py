""" Creates some random bingo cards. """
from random import sample, shuffle

import begin


def create_cards(numbers, amount, maximum):
    cards = []
    while len(cards) < amount:
        card = set(sample(range(1, maximum + 1), k=numbers))
        if card not in cards:
            cards.append(card)
    return cards


@begin.start(auto_convert=True)
def main(n: 'Numbers per card' = 25, a: 'Amount of cards' = 40,
         m: 'Maximum number' = 100, s: 'Shuffled' = True):
    """ Generates bingo cards """

    cards = create_cards(numbers=n, amount=a, maximum=m)
    print('The cards are:')
    for card in cards:
        card = list(card)
        shuffle(card) if s else None
        print(card)
