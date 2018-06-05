import time
import logging
from itertools import combinations

import begin

DICTS_DIR = '/home/rens/Projects/randomshit/Dictionaries/'
FILENAME = DICTS_DIR + 'Dutch.dic'


def find_word(word, words):
    return [x[:-1] for x in words if sorted(x[:-1]) == sorted(word)]


def find_combis(word, amount, words):
    combis = combinations(word, amount)
    options = list()
    for combi in combis:
        options.extend(find_word(combi, words))
    return list(set(options))


@begin.start(auto_convert=True)
@begin.logging
def main(w: 'Word', a: 'Amount of letters' = 0):
    """ Finds (Dutch) words with the given amount of letters. If 'l' is
    not given, it will use all letters in the given word. """
    start = time.time()
    a = a or len(w)

    with open(FILENAME) as f:
        words = list(f)

    combis = combinations(w, a)
    total_options = list()
    for combi in combis:
        options = find_word(combi, words)
        if options:
            total_options.extend(options)
            logging.debug('Combinatie: %s. Woorden: %s.', ''.join(combi), options)
    logging.info(f'{time.time() - start:.4} seconds')
    print(sorted(set(total_options)))
