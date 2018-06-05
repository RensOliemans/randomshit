import json
import os
from random import sample

import begin


current_dir = os.path.dirname(os.path.realpath(__file__))
filename = current_dir + '/dump.json'
proverbs = dict()
with open(filename) as f:
    proverbs = json.load(f)


@begin.start(auto_convert=True)
def main(a: 'Amount of proverbs' = 5, d: 'To define' = True):
    """ Gets some Dutch proverbs at random. """
    chosen = sample(proverbs.items(), a)
    if d:
        max_len = max([len(elem[0]) for elem in chosen]) + 4
        print('\n'.join(f'{elem[0]:{max_len}}{elem[1]}' for elem in chosen))
    else:
        print('\n'.join(choice[0] for choice in chosen))
