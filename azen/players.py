import random


class Player(object):
    """
    Superclass Player. This class is the main class for a user or AI that
    wishes to play the 'Azen' game
    """

    def __init__(self, username, ui):
        self.username = username
        self.end_score = 0
        self.ui = ui

    def __str__(self):
        return "Username: {0}".format(self.username)

    def __repr__(self):
        return "{0} object with username {1}".format("Player",
                                                     self.username)

    def make_move(self, board, verbose):
        raise NotImplementedError("make_move method is not impleemnted yet!")


class HumanPlayer(Player):
    """
    Subclass of the Player class, the HumanPlayer class.
    This is, as the name suggests, a class for a Human Player
    """
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        move = self.ui.ask_for_move(board)
        if move[0] == "move":
            location_of_first_card = move[1]
            location_of_empty_stack = move[2]
            board.move_card(location_of_first_card, location_of_empty_stack)
        elif move[0] == "remove":
            location_of_low_card = move[1]
            location_of_high_card = move[2]
            board.remove_card_location(location_of_low_card,
                                       location_of_high_card)
        elif move == "next":
            return "next"

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class NaivePlayer(Player):
    """
    Sublass of the Player class, the NaivePlayer class.
    This is the most simple AI. It checks if there are possible moves, and if
    so, it sets them. If not, it requests new cards.
    """
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        # Create a copy of the board before there are any changes.
        # old_board = copy.deepcopy(board)
        # board is Board object.
        # board.board is the field
        field = board.field
        if verbose >= 3:
            self.ui.show_board(board)
        for i in range(len(field)):
            if len(field[i]) != 0:
                first_card = field[i][-1]
                for j in range(len(field)):
                    if i != j and len(field[j]) != 0:
                        other_card = field[j][-1]
                        if first_card.suit == other_card.suit:
                            if first_card > other_card:
                                if verbose >= 3:
                                    print("Removing {0} using {1}"
                                          .format(other_card, first_card))
                                board.remove_card_location(j, i)
                                # Make a change, so start looking again
                                return self.make_move(board, verbose)
                            else:
                                if verbose >= 3:
                                    print("Removing {0} using {1}"
                                          .format(first_card, other_card))
                                board.remove_card_location(i, j)
                                # Make a change, so start looking again
                                return self.make_move(board, verbose)
        # No changes made (otherwise it would have returned) so return "next"
        if verbose >= 3:
            print("New cards")
        return "next"

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class MovingLargestPlayer(Player):
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        attempt_swap = False
        field = board.field
        if verbose >= 3:
            self.ui.show_board(board)
        for i in range(len(field)):
            if len(field[i]) != 0:
                first_card = field[i][-1]
                for j in range(len(field)):
                    if i != j:
                        if len(field[j]) != 0:
                            other_card = field[j][-1]
                            if first_card.suit == other_card.suit:
                                if first_card > other_card:
                                    if verbose >= 3:
                                        self.ui.show_board(board)
                                        print("Removing {0} using {1}"
                                              .format(other_card, first_card))
                                    board.remove_card_location(j, i)
                                    return self.make_move(board, verbose)
                                else:
                                    if verbose >= 3:
                                        self.ui.show_board(board)
                                        print("Removing {0} using {1}"
                                              .format(first_card, other_card))
                                    board.remove_card_location(i, j)
                                    return self.make_move(board, verbose)
                        else:
                            attempt_swap = True
            else:
                attempt_swap = True
        if attempt_swap:
            self.swap(board, verbose)
        if verbose >= 3:
            print("New cards")
        return "next"

    def swap(self, board, verbose):
        field = board.field
        filled_field = {i: field[i] for i in field if len(field[i]) > 1}
        try:
            index = max(filled_field.keys(),
                        key=lambda key: filled_field[key][0])
        except:
            return
        for i in range(len(field)):
            if len(field[i]) == 0:
                if verbose >= 3:
                    self.ui.show_board(board)
                    print("Index of card to swap: {0}, place to swap: {1}"
                          .format(index, i))
                board.move_card(index, i)
                return

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class MovingRandomPlayer(Player):
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        attempt_swap = False
        field = board.field
        if verbose >= 3:
            self.ui.show_board(board)
        for i in range(len(field)):
            if len(field[i]) != 0:
                first_card = field[i][-1]
                for j in range(len(field)):
                    if i != j:
                        if len(field[j]) != 0:
                            other_card = field[j][-1]
                            if first_card.suit == other_card.suit:
                                if first_card > other_card:
                                    if verbose >= 3:
                                        self.ui.show_board(board)
                                        print("Removing {0} using {1}"
                                              .format(other_card, first_card))
                                    board.remove_card_location(j, i)
                                    return self.make_move(board, verbose)
                                else:
                                    if verbose >= 3:
                                        self.ui.show_board(board)
                                        print("Removing {0} using {1}"
                                              .format(first_card, other_card))
                                    board.remove_card_location(i, j)
                                    return self.make_move(board, verbose)
                        else:
                            attempt_swap = True
            else:
                attempt_swap = True
        if attempt_swap:
            self.swap(board, verbose)
        if verbose >= 3:
            print("New cards")
        return "next"

    def swap(self, board, verbose):
        field = board.field
        filled_field = {i: field[i] for i in field if len(field[i]) > 1}
        try:
            number = random.randrange(1, len(filled_field))
            index = list(filled_field)[number]
        except:
            return
        for i in range(len(field)):
            if len(field[i]) == 0:
                if verbose >= 3:
                    self.ui.show_board(board)
                    print("Index of card to swap: {0}, place to swap: {1}"
                          .format(index, i))
                board.move_card(index, i)
                return

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class MovingSmallestPlayer(Player):
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        attempt_swap = False
        field = board.field
        if verbose >= 3:
            self.ui.show_board(board)
        for i in range(len(field)):
            if len(field[i]) != 0:
                first_card = field[i][-1]
                for j in range(len(field)):
                    if i != j:
                        if len(field[j]) != 0:
                            other_card = field[j][-1]
                            if first_card.suit == other_card.suit:
                                if first_card > other_card:
                                    if verbose >= 3:
                                        self.ui.show_board(board)
                                        print("Removing {0} using {1}"
                                              .format(other_card, first_card))
                                    board.remove_card_location(j, i)
                                    return self.make_move(board, verbose)
                                else:
                                    if verbose >= 3:
                                        self.ui.show_board(board)
                                        print("Removing {0} using {1}"
                                              .format(first_card, other_card))
                                    board.remove_card_location(i, j)
                                    return self.make_move(board, verbose)
                        else:
                            attempt_swap = True
            else:
                attempt_swap = True
        if attempt_swap:
            self.swap(board, verbose)
        if verbose >= 3:
            print("New cards")
        return "next"

    def swap(self, board, verbose):
        field = board.field
        filled_field = {i: field[i] for i in field if len(field[i]) > 1}
        try:
            number = random.randrange(1, len(filled_field))
            index = list(filled_field)[number]
        except:
            return
        for i in range(len(field)):
            if len(field[i]) == 0:
                if verbose >= 3:
                    self.ui.show_board(board)
                    print("Index of card to swap: {0}, place to swap: {1}"
                          .format(index, i))
                board.move_card(index, i)
                return

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


algorithms = {
    0: HumanPlayer,
    1: NaivePlayer,
    2: MovingLargestPlayer,
    3: MovingRandomPlayer,
    4: MovingSmallestPlayer,
}


def parse(message):
    for i in range(len(algorithms)):
        if message == str(i):
            return algorithms[i]
    raise ValueError("Wrong algorithm number.")
