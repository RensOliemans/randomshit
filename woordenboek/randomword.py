""" Prints a couple of random words from a dictionary. """
import logging
from concurrent.futures import ThreadPoolExecutor as Executor
from random import sample

import begin
import requests
import bs4


EN = "English (British).dic"
NL = "Dutch.dic"
DIR = "/home/rens/Projects/randomshit/Dictionaries/"
DICTS = {"EN": EN, "NL": NL}


def get_word(filename=EN, amount_of_words=5, length_of_words=0):
    """Gets a couple of words from a dictionary.

    :param filename: filename of the dictionary to use.
    :amount_of_words: amount of words you want returned
    :length_of_words: how long the words should be
    :returns: a list of words from the dictionary.
    """
    with open(DIR + filename) as dictionary:
        # strip last character; is '\n'
        if length_of_words:
            words = [x[:-1] for x in dictionary if len(x[:-1]) == length_of_words]
        else:
            # Don't care about word length
            words = [x[:-1] for x in dictionary]

    amount = min(len(words), amount_of_words)
    print(f"Amount of words with length {length_of_words}: {amount}\n")
    return sample(words, amount)


def define(word, language):
    """
    Defines a word

    :param word: the word to be defined
    :param language: the language of the words to define
    :returns: a list of definitions
    """
    texts = None
    if language == "EN":
        url = f"https://en.oxforddictionaries.com/definition/{word}"
        html = requests.get(url).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        # class_name where the definition is found
        class_name = "ind"
        # get definition items
        texts = [element.text for element in soup.findAll(attrs={"class": class_name})]
    elif language == "NL":
        url = f"https://www.vandale.nl/gratis-woordenboek/nederlands/betekenis/{word}"
        html = requests.get(url).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        class_name = "f0j"
        elements = soup.findAll(attrs={"class": class_name})
        # element has its definition as the last child
        # the first character of the definition is the number of the definition,
        # so remove that
        texts = [list(element.children)[-1].text[1:] for element in elements]
    return texts


@begin.start(auto_convert=True)
@begin.logging
def main(
    length: "Length of words. Leave 0 for any length" = 0,
    amount: "Amount of words" = 5,
    filename: "Filename" = "NL",
    to_define: "Define" = False,
):
    """Prints a couple of random words from a dictionary."""
    words = get_word(
        filename=DICTS[filename], length_of_words=length, amount_of_words=amount
    )
    logging.debug(words)
    if to_define:
        # multithread - multiple http requests, takes a while but can be done
        # multithreaded easily
        with Executor(max_workers=4) as exe:
            jobs = [exe.submit(define, word, filename) for word in words]
            defs = [job.result() for job in jobs]
        logging.debug(defs)
        # show only first definition
        defs = [defin[0] if defin else "" for defin in defs]
        logging.debug(defs)
        print("\n".join("\t".join(elem) for elem in zip(words, defs)))
    else:
        print("\n".join(words))
