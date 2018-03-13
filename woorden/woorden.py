import time
import sys
from itertools import combinations


def find_word(word, words):
    return [x[:-1] for x in words if sorted(x[:-1]) == sorted(word)]


def find_combis(word, amount, words):
    combis = combinations(word, amount)
    options = list()
    for combi in combis:
        options.extend(find_word(combi, words))
    return list(set(options))


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
    total_options = list()
    for combi in combis:
        options = find_word(combi, words)
        if options:
            total_options.extend(options)
            print('combinatie: {}. woorden: {}.'
                  .format(''.join(combi), options))
    print('{} seconds'.format(time.time() - start))
    print(total_options)


if __name__ == '__main__':
    dictionary_dic = '/home/rens/Projects/randomshit/Dictionaries/'
    filename = 'Dutch.dic'
    main(dictionary_dic + filename)
