import time
import sys
from itertools import combinations


def find_word(word, words):
    return [x[:-1] for x in words if sorted(x[:-1]) == sorted(word)]


def main(filename):
    with open(filename) as f:
        words = [x for x in f]
    word = input('Enter letters: ')

    try:
        amount = int(input('How many letters? '))
    except ValueError:
        print('No integer')
        sys.exit(1)

    start = time.time()
    combis = combinations(word, amount)
    for combi in combis:
        print('combinatie: {}. woorden: {}.'
              .format(''.join(combi), find_word(combi, words)))
    print('{} seconds'.format(time.time() - start))


if __name__ == '__main__':
    dictionary_dic = '/home/rens/Projects/randomshit/Dictionaries/'
    filename = 'Dutch.dic'
    main(dictionary_dic + filename)
