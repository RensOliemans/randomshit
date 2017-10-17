import random
import sys
import getopt
import os
import time

from random import shuffle


def run(amount_of_games=1000, rolls_per_game=30, verbose=False):
    start = time.time()
    # there are 40 tiles in a monopoly board, so the indices are 0-39
    tiles = [i for i in range(40)]
    tiles_count = dict()
    JAIL = 10
    GO_TO_JAIL = 30
    CHANCES = [7, 22, 26]
    CHESTS = [2, 17, 34]
    UTILITIES = [12, 28]
    RAILROADS = [5, 15, 25, 35]

    CHANCE_CARDS = [0, 24, 11, 'U', 'R', 40, 40, 'B', 10, 40, 40, 5,
                    39, 40, 40, 40]
    CHEST_CARDS = [0, 40, 40, 40, 40, 10, 40, 40, 40, 40, 40, 40, 40,
                   40, 40, 40, 40]

    for tile in tiles:
        tiles_count[tile] = 0

    chance = [i for i in CHANCE_CARDS]
    shuffle(chance)
    chest = [i for i in CHEST_CARDS]
    shuffle(chest)

    position = 0
    for game in range(amount_of_games):
        roll = 0
        position = 0
        doubles = 0
        jail_turns = 0
        double = False
        while roll < rolls_per_game:
            dice1 = random.randrange(1, 7)
            dice2 = random.randrange(1, 7)
            total = dice1 + dice2

            if dice1 == dice2:
                doubles += 1
                double = True
            else:
                doubles = 0
                double = False
            if doubles >= 3:
                position = JAIL

            # Following lines of code are if you want to have to throw doubles
            # to get out of jail
#            if position == JAIL:
#                if dice1 == dice2 or jail_turns >= 2:
#                    position = (position + total) % 40
#                    jail_turns = 0
#                else:
#                    jail_turns += 1
#            else:
#                position = (position + total) % 40

            # Following line of code is if you want to ignore the throwing of
            # doubles to get out of jail

            position = (position + total) % 40

            if position == GO_TO_JAIL:
                tiles_count[GO_TO_JAIL] += 1
                position = JAIL
            elif position in CHANCES:
                if chance == []:
                    # chance cards are empty, refill and shuffle
                    chance = [i for i in CHANCE_CARDS]
                    shuffle(chance)
                card = chance.pop(0)
                if not card == 40:
                    try:
                        position = int(card)
                    except ValueError:
                        if position == 'B':
                            # B indicates go back three places
                            position = (position - 3) % 40
                        elif position == 'U':
                            # U indicates go to the next utility card
                            for x in range(40):
                                if (position + x) % 40 in UTILITIES:
                                    position = (position + x) % 40
                        elif position == 'R':
                            # R indicates go to the next railroad card
                            for x in range(40):
                                if (position + x) % 40 in RAILROADS:
                                    position = (position + x) % 40
            elif position in CHESTS:
                if chest == []:
                    # chest cards are empty, refill and shuffle
                    chest = [i for i in CHEST_CARDS]
                    shuffle(chest)
                card = chest.pop(0)
                if not card == 40:
                    try:
                        position = int(card)
                    except ValueError as e:
                        print(e)

            if not double:
                roll += 1
            tiles_count[position] += 1

    result = ""
    throws = 0
    max_num = 0
    for item in tiles_count:
        throws += tiles_count[item]
        if tiles_count[item] > max_num:
            max_num = tiles_count[item]
    for item in tiles_count:
        result += "Item: {}, chance: {:.3%}\n".format(
                   item, (tiles_count[item] / throws))
    print(result)
    print("Running {:,} games (with {} rounds) took {:.3} seconds".format(
          amount_of_games, rolls_per_game, time.time() - start))


def parse_arguments(argv):
    amount_of_games = 1000
    rolls_per_game = 30
    verbose = False

    program_file = os.path.basename(__file__)
    usage_string = "Usage: python3 {} -g <amount_of_games> -r <rolls_per_game>"
    usage_string = usage_string.format(program_file)

    try:
        opts, args = getopt.getopt(argv, "hvg:r:")
    except getopt.GetoptError as e:
        print(usage_string)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(usage_string)
            sys.exit()
        elif opt == "-g":
            try:
                amount_of_games = int(arg)
            except ValueError:
                print("amount_of_games has to be a number")
                sys.exit(2)
        elif opt == "-r":
            try:
                rolls_per_game = int(arg)
            except ValueError:
                print("rolls_per_game has to be a number")
                sys.exit(2)
        elif opt == "-v":
            verbose = True
    return amount_of_games, rolls_per_game, verbose


if __name__ == "__main__":
    amount_of_games, rolls_per_game, verbose = parse_arguments(sys.argv[1:])
    run(amount_of_games, rolls_per_game, verbose)
