import ui
import game
import copy

class Player(object):
    """
    Superclass Player. This class is the main class for a user or AI that wishes
    to play the 'Azen' game
    """

    def __init__(self, username, ui):
        self.username = username
        self.end_score = 0
        self.ui = ui

    def __str__(self):
        return "Username: {0}".format(self.username)

    def make_move(self, board):
        raise NotImplementedError("make_move method is not impleemnted yet!")


class HumanPlayer(Player):
    """
    Subclass of the Player class, the HumanPlayer class.
    This is, as the name suggests, a class for a Human Player
    """
    def __init__(self, username, ui):
        super()

    def make_move(self, board):
        move = self.ui.ask_for_move(board)
        if move[0] == "move":
            location_of_first_card = move[1]
            location_of_empty_stack = move[2]
            board.move_card(location_of_first_card, location_of_empty_stack)
        elif move[0] == "remove":
            location_of_low_card = move[1]
            location_of_high_card = move[2]
            board.remove_card(location_of_low_card, location_of_high_card)
        elif move == "next":
            return 1

    def invalid_move(self, board):
        self.ui.show_invalid_move(board)


class NaivePlayer(Player):
    """
    Sublass of the Player class, the NaivePlayer class.
    This is the most simple AI. It checks if there are possible moves, and if
    so, it sets them. If not, it requests new cards.
    """
    def __init__(self, username, ui):
        super()

    def make_move(self, board):
        # Create a copy of the board before there are any changes.
        # old_board = copy.deepcopy(board)
        # board is Board object.
        # board.board is the field
        field = board.board
        for i in range(len(field)):
            if len(field[i]) != 0:
                first_card = field[i][-1]
                for j in range(len(field)):
                    if i != j and len(field[j]) != 0:
                        other_card = field[j][-1]
                        if first_card.suit == other_card.suit:
                            if first_card > other_card:
                                board.remove_card(j, i)
                                # Make a change, so start looking again
                                return self.make_move(board)
                            else:
                                board.remove_card(i, j)
                                # Make a change, so start looking again
                                return self.make_move(board)
        # No changes made (otherwise it would have returned) so return "next"
        return "next"

    def invalid_move(self, board):
        self.ui.show_invalid_move(board)

class FastNaivePlayer(Player):
    pass
