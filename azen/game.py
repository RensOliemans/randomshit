import sys
import time
import math

import cards.deck as card_deck
from azenerrors import InvalidMoveException
import players
import uis


class Board(object):
    """
    The board object. It has four lists of cards.
    """

    def __init__(self, cards=None, deck=None, stacks=4):
        """
        Board constructor method.

        :arg cards:
            The lists of cards. Should be a dictionary with four lists.
        :arg deck:
            The deck of cards, if you want a specifically shuffled
            (or sorted) deck of cards.
        """
        self.deck = deck or card_deck.Deck()
        self.deck.shuffle()
        if len(self.deck.cards) % stacks != 0:
            raise ValueError("Deck has to be divisible by amount of stacks")
        self.stacks = stacks
        if cards:
            self.field = cards
        else:
            self.field = dict()
            for i in range(self.stacks):
                self.field[i] = list()

    def __str__(self):
        """
        Returns a string representation of the board
        """
        result = ""
        for i in range(self.stacks):
            result += "Stack {0}: ".format(i)
            for card in self.field[i][::-1]:
                result += "{0}\t".format(card)
            result += "\n"
        return result

    def __repr__(self):
        """
        Returns a representation of the Board object.
        """
        result = "Board: (Stack 1: {b[0]}, Stack 2: {b[1]}, " + \
                 "Stack 3: {b[2]}, Stack 4: {b[3]}"
        return result.format(b=self.field)

    def add_cards(self):
        """
        Adds a card on each of the stacks from the deck.
        """
        for i in range(self.stacks):
            self.field[i] += self.deck.deal(1)

    def remove_card(self, low_card, high_card):
        """
        Removes a card, when two cards are given.
        Requires the cards to have the same suits, and the first argument
        (low_card) to have a lower value than the second argument (high_card).

        :arg ``Card`` low_card:
            Card object with the lower value.
        :arg ``Card`` high_card:
            Card object with the higher value.
        """
        location_of_low_card = 0
        location_of_high_card = 0
        for i in range(len(self.field)):
            if low_card in self.field[i]:
                location_of_low_card = i
            if high_card in self.field[i]:
                location_of_high_card = i
        self.remove_card_location(location_of_low_card, location_of_high_card)

    def remove_card_location(self,
                             location_of_low_card, location_of_high_card):
        """
        Removes a card. This requires there to be a card with a higher value,
        in the same suit as a card of the card you want to remove (low value).

        :arg int location_of_low_card:
            Stack of the low card (has to be on top)
        :arg int location_of_high_card:
            Stack of the high card (has to be on top)
        """
        if location_of_low_card == location_of_high_card:
            raise InvalidMoveException("You have to give two different stacks")
        if (len(self.field[location_of_low_card]) == 0
                or len(self.field[location_of_high_card]) == 0):
            raise InvalidMoveException(
                "{0} or {1} can't be zero!".format(location_of_low_card,
                                                   location_of_high_card)
            )
        if (location_of_low_card > self.stacks
           or location_of_high_card > self.stacks):
            raise InvalidMoveException(
                "{0} or {1} can't be larger than the amount of stacks!".format(
                    location_of_low_card, location_of_high_card)
            )
        low_card = self.field[location_of_low_card][-1]
        high_card = self.field[location_of_high_card][-1]
        if high_card.suit != low_card.suit or high_card < low_card:
            raise InvalidMoveException("Can't remove a {0} with a {1}!".format(
                                        high_card, low_card))
        # print("removing {0}".format(self.field[location_of_low_card][-1]))
        del self.field[location_of_low_card][-1]

    def move_card(self, location_of_card, location_of_empty_stack):
        """
        Moves a card to an empty stack.

        :arg int location_of_first_card:
            Location of the card that has to be moved.
        :arg int location_of_empty_stack:
            Location of the empty stack that the card has to be moved to.
        """
        if (location_of_card >= self.stacks
           or location_of_empty_stack >= self.stacks):
            raise InvalidMoveException("Stack out of range!")
        if len(self.field[location_of_empty_stack]) != 0:
            raise InvalidMoveException(
                    "Stack {0} isn't empty!".format(location_of_empty_stack)
            )
        if len(self.field[location_of_card]) == 0:
            raise InvalidMoveException(
                    "There is no card on stack {0}!"
                    .format(location_of_card)
            )
        first_card = self.field[location_of_card][-1]
        del self.field[location_of_card][-1]
        self.field[location_of_empty_stack].append(first_card)

    def is_game_over(self):
        return len(self.deck.cards) == 0

    def end_score(self):
        end_score = 0
        for i in range(self.stacks):
            end_score += len(self.field[i])
        return end_score


def main(algorithm, loops=1, verbose=0):
    total_score = 0
    completions = 0
    ten_percent_mark = math.ceil(loops / 10)
    percent = 0
    for i in range(loops):
        if verbose >= 1 and i != 0 and i % ten_percent_mark == 0:
            percent += 10
            print("{}%".format(percent))
        board = Board()
        player_ui = uis.TUI()
        rens = algorithm("rens", player_ui)
        game_over = board.is_game_over()
        while not game_over:
            board.add_cards()
            choice = -1
            while choice != "next":
                try:
                    choice = rens.make_move(board, verbose)
                except InvalidMoveException as inst:
                    print(inst)
                    rens.invalid_move(board, verbose)
                    # choice = rens.make_move(board)
            game_over = board.is_game_over()
        end_score = board.end_score()
        total_score += end_score
        if end_score == 4:
            if verbose >= 1:
                print("COMPLETED!")
            completions += 1
        if verbose >= 2:
            print("----------------END OF GAME, SCORE: {0}---------------"
                  .format(end_score))
    if verbose >= 1:
        print("Average score: {0}".format(total_score / loops))
        print("Completions: {0}".format(completions))
        print("Percent of completion: {0}%".format(completions / loops))


def handle_arguments():
    algorithm = players.NaivePlayer
    loops = 1
    verbose = 0

    default_message = "Incorrect number, using default {default}"
    help_arguments = ['-h', '--help']
    if len(sys.argv) > 1:
        for i in range(len(sys.argv)):
            argument = sys.argv[i]
            if argument == '-a':
                try:
                    algorithm = players.parse(sys.argv[i + 1])
                except:
                    message = "Available algorithms: \n{algorithms}\n"
                    print((default_message + "\n" + message)
                          .format(algorithms=players.algorithms,
                                  default="algorithm"))
            elif argument == '-l':
                try:
                    loops = int(sys.argv[i + 1])
                    if loops <= 0:
                        raise Exception
                except:
                    loops = 1
                    print(default_message.format(default="loops"))
            elif argument[:2] == '-v':
                verbose = argument.count('v')
            elif argument in help_arguments:
                usage()
    return algorithm, loops, verbose


def usage():
    message = "Usage: python game.py [-a algorithm_number] [-l loops]"
    print(message)


if __name__ == "__main__":
    algorithm, loops, verbose = handle_arguments()
    start = time.time()
    main(algorithm, loops, verbose)
    if verbose >= 1:
        print("Program took {0} seconds for {1} loops with algorithm {2}"
              .format(time.time() - start, loops, repr(algorithm)))
