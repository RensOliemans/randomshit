import cards.deck as card_deck
from azenerrors import InvalidMoveException
from players import HumanPlayer
import ui

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
            self.board = cards
        else:
            self.board = dict()
            for i in range(self.stacks):
                self.board[i] = list()

    def __str__(self):
        """
        Returns a string representation of the board
        """
        result = ""
        for i in range(self.stacks):
            result += "Stack {0}: ".format(i)
            for card in self.board[i]:
                result += "{0}\n".format(card)
            result += "\n"
        return result

    def __repr__(self):
        """
        Returns a representation of the Board object.
        """
        result = "Board: (Stack 1: {b[0]}, Stack 2: {b[1]}, " + \
                 "Stack 3: {b[2]}, Stack 4: {b[3]}"
        return result.format(b=self.board)

    def add_cards(self):
        """
        Adds a card on each of the stacks from the deck.
        """
        for i in range(self.stacks):
            self.board[i] += self.deck.deal(1)

    def remove_card(self, location_of_low_card, location_of_high_card):
        """
        Removes a card. This requires there to be a card with a higher value,
        in the same suit as a card of the card you want to remove (low value).

        :arg int location_of_low_card:
            Stack of the low card (has to be on top)
        :arg int location_of_high_card:
            Stack of the high card (has to be on top)
        """
        if location_of_low_card == location_of_high_card:
            raise InvalidMoveException("You have to give two different stacks!")
        high_card = self.board[location_of_high_card][-1]
        low_card = self.board[location_of_low_card][-1]
        if high_card.suit != low_card.suit or high_card.value < low_card.value:
            raise InvalidMoveException("Can't remove a {0} with a {1}!".format(
                                        high_card, low_card))
        del self.board[location_of_low_card][-1]

    def move_card(self, location_of_first_card, location_of_empty_stack):
        """
        Moves a card to an empty stack.

        :arg int location_of_first_card:
            Location of the card that has to be moved.
        :arg int location_of_empty_stack:
            Location of the empty stack that the card has to be moved to.
        """
        if len(self.board[location_of_empty_stack]) != 0:
            raise InvalidMoveException(
                    "Stack {0} isn't empty!".format(location_of_empty_stack)
            )
        if len(self.board[location_of_first_card]) == 0:
            raise InvalidMoveException(
                    "There is no card on stack {0}!".format(location_of_first_card)
            )
        first_card = self.board[location_of_first_card][-1]
        del self.board[location_of_first_card][-1]
        self.board[location_of_empty_stack].append(first_card)

    def is_game_over(self):
        return len(self.deck.cards) == 0

    def end_score(self):
        end_score = 0
        for i in range(self.stacks):
            end_score += len(self.board[i])
        return end_score

def main():
    board = Board()
    player_ui = ui.TUI()
    rens = HumanPlayer("rens", player_ui)
    game_over = board.is_game_over()
    while not game_over:
        rens.make_move(board)
        game_over = board.is_game_over()
    end_score = board.end_score()
    print("Your end score: {0}".format(end_score))

if __name__ == "__main__":
    main()
