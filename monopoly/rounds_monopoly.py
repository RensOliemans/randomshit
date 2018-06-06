import time
from random import shuffle, randrange

import begin
from tqdm import tqdm

games = 0

# these all refer to the locations on the board
JAIL = 10
GO_TO_JAIL = 30
CHANCES = [7, 22, 26]
CHESTS = [2, 17, 34]
UTILITIES = [12, 28]
RAILROADS = [5, 15, 25, 35]

# these refer to the location jumping the chance/chest cards send you to
CHANCE_CARDS = [0, 24, 11, 'U', 'R', 40, 40, 'B', 10, 40, 40, 5,
                39, 40, 40, 40]
CHEST_CARDS = [0, 40, 40, 40, 40, 10, 40, 40, 40, 40, 40, 40, 40,
               40, 40, 40, 40]


def run(rolls_per_game=30, excel=False):
    global games
    games += 1
    # start = time.time()
    # there are 40 tiles in a monopoly board, so the indices are 0-39
    tiles_count = {x: 0 for x in range(40)}

    chance = list(CHANCE_CARDS)
    shuffle(chance)
    chest = list(CHEST_CARDS)
    shuffle(chest)

    position = 0

    roll = 0
    position = 0
    doubles = 0
    # jail_turns = 0
    double = False
    while roll < rolls_per_game:
        dice1 = randrange(1, 7)
        dice2 = randrange(1, 7)
        total = dice1 + dice2

        if dice1 == dice2:
            doubles += 1
            double = True
        else:
            doubles = 0
            double = False
        if doubles >= 3:
            position = JAIL

        # Following if statement is if you want to have to throw doubles
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
            if not chance:
                # chance cards are empty, refill and shuffle
                chance = list(CHANCE_CARDS)
                shuffle(chance)
            card = chance.pop(0)
            # 40 means no jumping
            if not card == 40:
                try:
                    tiles_count[position] += 1
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
            if not chest:
                # chest cards are empty, refill and shuffle
                chest = list(CHEST_CARDS)
                shuffle(chest)
            card = chest.pop(0)
            # 40 means no jumping
            if not card == 40:
                position = int(card)

        if not double:
            roll += 1
        tiles_count[position] += 1

    return tiles_count
    # print(result)
    # print("Running {:,} games (with {} rounds) took {:.3} seconds".format(
    #     amount_of_games, rolls_per_game, time.time() - start))


def pretty_format(tiles_count, excel=False):
    throws = sum([tiles_count[x] for x in tiles_count])
    result = ""
    if excel:
        result += "Item;chance\n"
    for item in tiles_count:
        if excel:
            result += "{};{:.3%}\n".format(
                item, (tiles_count[item] / throws))
        else:
            result += "Item: {}, chance: {:.3%}\n".format(
                item, (tiles_count[item] / throws))
    return result


@begin.start(auto_convert=True)
def main(g: 'Amount of games' = 1000, r: 'Rolls per game' = 30,
         e: 'Format Excel-friendly' = False):
    """ Simulates monopoly games and outputs the frequency of the tiles
    visited, including jail workings and chance/community cards. """
    start = time.time()
    dicts = list()
    for _ in tqdm(range(g)):
        dicts.append(run(r, e))
    end_dict = {k: sum(d[k] for d in dicts) for k in dicts[0]}
    print(pretty_format(end_dict, e))
    print("Running {:,} games (with {} rounds) took {:.3} seconds".format(
          g, r, time.time() - start))
