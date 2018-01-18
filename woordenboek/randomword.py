import os
import sys
import getopt

from random import sample

EN = "en_EN.dic"
NL = "nl_NL.dic"
DIR = "dicts/"


def get_word(filename=EN, amount_of_words=5, length_of_words=10):
    words = list()
    with open(DIR + filename) as f:
        words = [x[:-1] for x in f if len(x) == length_of_words]

    amount = min(len(words), amount_of_words)
    print("Amount of words with length {}: {}\n".format(
          length_of_words, amount))
    return sample(words, min(len(words), amount_of_words))


def parse_arguments(argv):
    # DEFAULT VALUES
    length_of_words = 10
    amount_of_words = 5
    filename = EN
    # END OF DEFAULT VALUES

    program_file = os.path.basename(__file__)
    usage_string = ("Usage: python3 {} "
                    "-l <length_of_words> "
                    "-a <amount_of_words> ").format(program_file)

    help_string = ("<length_of_words> is the amount of characters in a word\n"
                   "<amount_of_words> means the amount of words printed\n")

    try:
        opts, args = getopt.getopt(argv, "hl:a:")
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
    return length_of_words, amount_of_words, filename


def main():
    length_of_words, amount_of_words, filename = parse_arguments(sys.argv[1:])
    words = get_word(
            filename=filename,
            length_of_words=length_of_words,
            amount_of_words=amount_of_words)
    print('\n'.join(words))


if __name__ == "__main__":
    main()
