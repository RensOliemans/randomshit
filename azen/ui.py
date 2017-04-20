class UI(object):
    """
    A UI superclass, that can be extended for a TUI or GUI
    """
    def __init__(self):
        pass

    def show_board(self, board):
        raise NotImplementedError

    def ask_for_move(self, board):
        raise NotImplementedError

class TUI(UI):
    """
    Subclass of the UI class, a Textual User Interface.
    """
    def show_board(self, board):
        print("The board is: {0}".format(board))

    def ask_for_move(self, board):
        choice = input("Do you want to move a card or remove a card?")
        if choice.lower() == "move" or choice == "0":
            card = input("From what stack do you want to move a card?")
            location = input("To what stack do you want to move the card?")
            return ("move", card, location)
        elif choice.lower() == "remove" or choice == "1":
            smaller_card = input("What stack contains the SMALLER card?")
            larger_card = input("What stack contains the larger card?")
            return ("remove", smaller_card, larger_card)
        else:
            message = "Incorrect option. Use 'move' or '0' to move, and " + \
                      "'remove' or '1' to remove."
            print(message)
            return ask_for_move(self, board)
