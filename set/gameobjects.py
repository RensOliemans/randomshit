import Set
import constants

from enum import Enum
from random import shuffle


class Card(object):

    """This method represents a Card in the game Set."""

    def __init__(self, colour, form, amount, fill):
        """Each card has four attributes that make the card unique.

        :colour: The colour, Enum. Values can be found in Color.
        :form: The form, Enum. Values can be found in Form.
        :amount: The amount of icons on a card, can be 1, 2 or 3.
        :fill: The fill, Enum. VAlues can be found in Fill.
        """
        self.colour = colour
        self.form = form
        self.amount = amount
        self.fill = fill

    def __add__(self, other):
        sames = list()
        if self.colour == other.colour:
            sames.append(type(self.colour))
        if self.form == other.form:
            sames.append(type(self.form))
        if self.amount == other.amount:
            sames.append(type(self.amount))
        if self.fill == other.fill:
            sames.append(type(self.fill))
        return sames

    def __sub__(self, other):
        diffs = list()
        if self.colour != other.colour:
            diffs.append(type(self.colour))
        if self.form != other.form:
            diffs.append(type(self.form))
        if self.amount != other.amount:
            diffs.append(type(self.amount))
        if self.fill != other.fill:
            diffs.append(type(self.fill))
        return diffs

    def __eq__(self, other):
        return (self.colour == other.colour and self.form == other.form
                and self.amount == other.amount and self.fill == other.fill)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "Card. Colour: {}, Amount: {}, Fill: {}, Form: {}.".format(
                self.colour.name, self.amount, self.fill.name,
                self.form.name)

    def __str__(self):
        return "{}, {}, {} card with amount {}".format(
                self.colour.name, self.form.name, self.fill.name,
                self.amount)


class Colour(Enum):
    RED = 1
    PURPLE = 2
    GREEN = 3


class Form(Enum):
    SQWIGGLE = 1
    SQUARE = 2
    CIRCLE = 3


class Fill(Enum):
    EMPTY = 0
    DOTTED = 1
    FILLED = 2


class Deck(object):

    """This deck represents the deck of Set cards for the game Set"""

    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        cards = list()
        for col in Colour:
            for form in Form:
                for fill in Fill:
                    for amount in range(1, constants.GAME_AMOUNT + 3):
                        card = Card(col, form, amount, fill)
                        cards.append(card)
        shuffle(cards)
        return cards

    def take(self, n=1):
        cards = list()
        for _ in range(n):
            try:
                cards.append(self.cards.pop())
            except IndexError:
                pass
        return cards


BOARD_SIZE = constants.GAME_AMOUNT * constants.GAME_AMOUNT


class Board(object):

    def __init__(self):
        self.deck = Deck()
        self.board = self.deck.take(BOARD_SIZE)

    def remove_cards(self, cards):
        if not len(cards) == constants.GAME_AMOUNT:
            return
        if Set.is_set(cards):
            for card in cards:
                self.board.remove(card)

    def extra_cards(self):
        self.board += self.deck.take(constants.GAME_AMOUNT)
