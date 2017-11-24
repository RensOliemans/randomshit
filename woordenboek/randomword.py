import io
import os
import sys
import getopt

from random import shuffle

NL = "nl_NL.dic"
EN = "en_EN.dic"
DIR = "dicts/"


def get_word(lang=NL, amount_of_words=5, length_of_words=10):
    f = io.open(DIR + lang, encoding='latin-1')
    words = list()
    for word in f:
        word = word[:-1]
        if "/" in word:
            index = len(word) - word.index("/")
            word = word[:-index]
        words.append(word)
    f.close()
    word = ""
    # we only want long words
    correct_length_words = [x for x in words if len(x) == length_of_words]
    shuffle(correct_length_words)
    print("Amount of words with length {}: {}\n".format(
          length_of_words, len(correct_length_words)))
    return correct_length_words[:amount_of_words]


def parse_arguments(argv):
    length_of_words = 10
    amount_of_words = 5
    lang = EN

    program_file = os.path.basename(__file__)
    usage_string = "Usage: python3 {} " \
                   "-l <length_of_words> " \
                   "-a <amount_of_words> " \
                   "-t <language>".format(program_file)

    help_string = "<length_of_words> is the amount of characters in a word\n" \
                  "<amount_of_words> means the amount of words printed\n" \
                  "<language> is the language of the words, NL or EN."

    try:
        opts, args = getopt.getopt(argv, "ht:l:a:")
    except getopt.GetoptError as e:
        print(usage_string)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(usage_string)
            print(help_string)
            sys.exit()
        elif opt == "-l":
            try:
                length_of_words = int(arg)
            except ValueError:
                print("length_of_words has to be a number")
                sys.exit(2)
        elif opt == "-a":
            try:
                amount_of_words = int(arg)
            except ValueError:
                print("amount_of_words has to be a number")
                sys.exit(2)
        elif opt == "-t":
            if arg == "NL":
                lang = NL
            else:
                lang = EN
    return length_of_words, amount_of_words, lang


if __name__ == "__main__":
    length_of_words, amount_of_words, lang = parse_arguments(sys.argv[1:])
    words = get_word(
            lang=lang,
            length_of_words=length_of_words,
            amount_of_words=amount_of_words)
    for word in words:
        print(word)
