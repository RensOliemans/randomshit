class UI(object):
    """
    A UI superclass, that can be extended for a TUI or GUI
    """
    def __init__(self):
        pass

    def show_board(self, board, additional_message=""):
        raise NotImplementedError

    def ask_for_move(self, board):
        raise NotImplementedError

    def show_invalid_move(self, board):
        raise NotImplementedError


class TUI(UI):
    """
    Subclass of the UI class, a Textual User Interface.
    """
    def __init__(self):
        pass

    def show_board(self, board, additional_message=""):
        message = "The board is: \n{0}There are {1} cards left{2}\n"
        print(message.format(board, len(board.deck.cards), additional_message))

    def ask_for_move(self, board):
        self.show_board(board)
        print("Options: move, remove, next")
        choice = input("Do you want to move a card or remove a card? ")
        if choice.lower() == "move" or choice == "0" or choice == "m":
            card = input("From what stack do you want to move a card? ")
            location = input("To what stack do you want to move the card? ")
            try:
                int(card), int(location)
            except ValueError:
                print("Incorrect option. Try again.")
                return self.ask_for_move(board)
            return ("move", int(card), int(location))
        elif choice.lower() == "remove" or choice == "1" or choice == "r":
            smaller_card = input("What stack contains the SMALLER card? ")
            larger_card = input("What stack contains the LARGER card? ")
            try:
                int(smaller_card), int(larger_card)
            except ValueError:
                print("Incorrect option. Try again.")
                return self.ask_for_move(board)
            return ("remove", int(smaller_card), int(larger_card))
        elif choice.lower() == "next" or choice == "2" or choice == "n":
            return ("next")
        else:
            message = "Incorrect option. Use 'move' or '0' to move, and " + \
                    "'remove' or '1' to remove."
            print(message)
            return self.ask_for_move(board)

    def show_invalid_move(self, board):
        print("Incorrect move! Try again.")
