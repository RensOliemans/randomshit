import begin
import lxml.html
import logging
from urllib.request import urlopen
from urllib.error import HTTPError

from random import sample

EN = 'English (British).dic'
NL = 'Dutch.dic'
DIR = '/home/rens/Projects/randomshit/Dictionaries/'


def get_word(filename=EN, amount_of_words=5, length_of_words=10):
    words = list()
    with open(DIR + filename) as f:
        # strip last character: is '\n'
        words = [x[:-1] for x in f if len(x[:-1]) == length_of_words]

    amount = min(len(words), amount_of_words)
    print("Amount of words with length {}: {}\n".format(
          length_of_words, amount))
    return sample(words, amount)


def define(word):
    # get html page
    try:
        html = urlopen('https://en.oxforddictionaries.com/definition/' + word).read()
    except HTTPError:
        logging.error('ERROR: ' + word)
        return []
    # get definition items
    elements = lxml.html.fromstring(str(html)).find_class('ind')
    texts = [elem.text.strip() for elem in elements
             if elem.text is not None]
    return texts


@begin.start(auto_convert=True)
@begin.logging
def main(l: 'Length of words' = 10, a: 'Amount of words' = 5,
         f: 'Filename' = "{}".format(EN), d: 'Define' = False):
    words = get_word(filename=f, length_of_words=l, amount_of_words=a)
    logging.debug(words)
    if d:
        defs = [define(word) if len(define(word)) > 0 else ''
                for word in words]
        logging.debug(defs)
        defs = [defin[0] if len(defin) > 0 else '' for defin in defs]
        logging.debug(defs)
        logging.debug('')
        print('\n'.join('\t'.join(elem) for elem in zip(words, defs)))
    else:
        print('\n'.join(words))
