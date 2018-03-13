import begin

from random import sample

EN = "English (British).dic"
NL = 'Dutch.dic'
DIR = "/home/rens/Projects/randomshit/Dictionaries/"


def get_word(filename=EN, amount_of_words=5, length_of_words=10):
    words = list()
    with open(DIR + filename) as f:
        # strip last character: is '\n'
        words = [x[:-1] for x in f if len(x[:-1]) == length_of_words]

    amount = min(len(words), amount_of_words)
    print("Amount of words with length {}: {}\n".format(
          length_of_words, amount))
    return sample(words, amount)


@begin.start(auto_convert=True)
def main(l: 'Length of words' = 10, a: 'Amount of words' = 5,
         f: 'Filename' = "'{}'".format(EN)):
    words = get_word(filename=f, length_of_words=l, amount_of_words=a)
    print('\n'.join(words))
