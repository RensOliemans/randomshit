import sys
import getopt
import os

from random import sample, shuffle
from scipy.special import binom


def create_cards(numbers, amount, maximum):
    cards = []
    while len(cards) < amount:
        card = set(sample(range(1, maximum + 1), k=numbers))
        if card not in cards:
            cards.append(card)
    return cards


def parse_arguments(argv):
    numbers_per_card = 5 * 5   # usually 25 numbers per bingo card
    amount_of_cards = 40       # amount of cards you want to generate
    maximum_number = 100       # default max bingo number on the cards
    print_shuffled = False

    program_file = os.path.basename(__file__)
    usage_string = "Usage: python3 {} " \
                   "-n <numbers_per_card> " \
                   "-a <amount_of_cards> " \
                   "-m <maximum_number> " \
                   "-s <shuffled>".format(program_file)

    help_string = "<numbers_per_card> is the bingo numbers you want on the card, " \
                  "defaults to {}.\n" \
                  "<amount_of_cards> is the amount of cards you want to generate, " \
                  "defaults to {}.\n" \
                  "<maximum_number> is the maximum bingo number on the cards, " \
                  "defaults to {}.\n" \
                  "<shuffled> is a flag if you want to have the cards shuffled or not" \
                  "".format(numbers_per_card, amount_of_cards, maximum_number)

    try:
        opts, args = getopt.getopt(argv, "hsn:a:m:")
    except getopt.GetoptError:
        print(usage_string)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(usage_string)
            print(help_string)
            sys.exit()
        elif opt == "-s":
            print_shuffled = True
        elif opt == "-n":
            try:
                numbers_per_card = int(arg)
            except ValueError:
                print("numbers_per_card has to be a number")
                sys.exit(2)
        elif opt == "-a":
            try:
                amount_of_cards = int(arg)
            except ValueError:
                print("amount_of_cards has to be a number")
                sys.exit(2)
        elif opt == "-m":
            try:
                maximum_number = int(arg)
            except ValueError:
                print("maximum_number has to be a number")
                sys.exit(2)
    if maximum_number < numbers_per_card:
        print("maximum_number has to be larger than numbers_per_card")
        sys.exit(2)
    if binom(maximum_number, numbers_per_card) < amount_of_cards:
        print("Can't create enough permutations with these parameters to ensure "
              "that all cards are unique")
        sys.exit(2)
    return (numbers_per_card, amount_of_cards, maximum_number, print_shuffled)


if __name__ == "__main__":
    numbers_per_card, amount_of_cards, maximum_number, print_shuffled = parse_arguments(sys.argv[1:])
    cards = create_cards(
            numbers=numbers_per_card,
            amount=amount_of_cards,
            maximum=maximum_number)
    print("The cards are:")
    for card in cards:
        card = list(card)
        if print_shuffled:
            shuffle(card)
        print(card)
