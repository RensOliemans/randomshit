""" Prints a couple of random words from a dictionary. """
import logging
from concurrent.futures import ThreadPoolExecutor as Executor
from random import sample

import begin
import requests
import lxml.html


EN = 'English (British).dic'
NL = 'Dutch.dic'
DIR = '/home/rens/Projects/randomshit/Dictionaries/'


def get_word(filename=EN, amount_of_words=5, length_of_words=10):
    """ Gets a couple of words from a dictionary.

    :param filename: filename of the dictionary to use.
    :amount_of_words: amount of words you want returned
    :length_of_words: how long the words should be
    :returns: a list of words from the dictionary.
    """
    with open(DIR + filename) as dictionary:
        # strip last character; is '\n'
        words = [x[:-1] for x in dictionary if len(x[:-1]) == length_of_words]

    amount = min(len(words), amount_of_words)
    print("Amount of words with length {}: {}\n".format(
        length_of_words, amount))
    return sample(words, amount)


def define(word):
    """
    Defines a word

    :param word: the word to be defined
    :returns: a list of definitions
    """
    # get html page
    html = requests.get('https://en.oxforddictionaries.com/definition/' + word)
    # get definition items
    class_name = 'ind'
    elements = lxml.html.fromstring(html.text).find_class(class_name)
    texts = [elem.text.strip() for elem in elements
             if elem.text is not None]
    return texts


@begin.start(auto_convert=True)
@begin.logging
def main(length: 'Length of words' = 10,
         amount: 'Amount of words' = 5,
         filename: 'Filename' = "{}".format(EN),
         to_define: 'Define' = False):
    """ Prints a couple of random words from a dictionary. """
    words = get_word(filename=filename,
                     length_of_words=length, amount_of_words=amount)
    logging.debug(words)
    if to_define:
        with Executor(max_workers=4) as exe:
            jobs = [exe.submit(define, word) for word in words]
            defs = [job.result() for job in jobs]
        logging.debug(defs)
        # take first definition
        defs = [defin[0] if defin else ''
                for defin in defs]
        logging.debug(defs)
        print('\n'.join('\t'.join(elem) for elem in zip(words, defs)))
    else:
        print('\n'.join(words))
