import io
import os
import sys
import getopt

from random import shuffle


def get_word(filename="nl_NL.dic", amount_of_words=5, length_of_words=10):
    f = io.open(filename, encoding='latin-1')
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

    program_file = os.path.basename(__file__)
    usage_string = "Usage: python3 {} -l <length_of_words> " \
                   " -a <amount_of_words>".format(program_file)

    try:
        opts, args = getopt.getopt(argv, "hl:a:")
    except getopt.GetoptError as e:
        print(usage_string)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(usage_string)
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
    return length_of_words, amount_of_words


if __name__ == "__main__":
    length_of_words, amount_of_words = parse_arguments(sys.argv[1:])
    words = get_word(
            length_of_words=length_of_words,
            amount_of_words=amount_of_words)
    for word in words:
        print(word)
