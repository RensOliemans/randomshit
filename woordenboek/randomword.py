import begin
import lxml.html
import logging
import requests
from concurrent.futures import ThreadPoolExecutor as Executor

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
    html = requests.get('https://en.oxforddictionaries.com/definition/' + word).text
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
        with Executor(max_workers=4) as exe:
            jobs = [exe.submit(define, word) for word in words]
            defs = [job.result() for job in jobs]
        logging.debug(defs)
        # take first definition
        defs = [defin[0] if len(defin) > 0 else '' for defin in defs]
        logging.debug(defs)
        print('\n'.join('\t'.join(elem) for elem in zip(words, defs)))
    else:
        print('\n'.join(words))
