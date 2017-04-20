import ui

class Player(object):
    """
    Superclass Player. This class is the main class for a user or AI that wishes
    to play the 'Azen' game
    """

    def __init__(self, username):
        self.username = username
        self.end_score = 0

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
        self.ui = ui

    def make_move(self, board):
        ui.show_board(board)
        move = ui.ask_for_move(board)
        if move[0] == "move":
            location_of_first_card = move[1]
            location_of_empty_stack = move[2]
            board.move_card(location_of_first_card, location_of_empty_stack)
        elif move[1] == "remove":
            location_of_low_card = move[1]
            location_of_high_card = move[2]
            board.remove_card(location_of_low_card, location_of_high_card)

