import random

from random import shuffle

from exceptions import NoOwnerAndHousesException, HousesYetMortgagedException


class Board(object):
    """
    This class models the monopoly board. It keeps track of the current
    position of players, chance/community cards, properties owned
    by whom, houses placed, etc.
    """
    CHANCE = [0, 24, 11, 'U', 'R', 40, 40, 'B', 10, 40, 40, 5, 39, 40, 40, 40]
    COMMUNITY = [0, 40, 40, 40, 40, 10, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
                 40]
    GO = 0
    JAIL = 10
    FREE_PARKING = 20
    GO_TO_JAIL = 30

    def __init__(self, players):
        self.community = [i for i in self.COMMUNITY]
        self.chance = [i for i in self.CHANCE]

        self.players = players
        self.current_player = 0

        self.reshuffle_chances()
        self.reshuffle_community()

    def reshuffle_chances(self):
        """
        Refills and shuffles the chance card pile
        """
        self.chance = [i for i in self.CHANCE]
        shuffle(self.chance)

    def reshuffle_community(self):
        """
        Refills and shuffles the community card pile
        :return:
        """
        self.community = [i for i in self.COMMUNITY]
        shuffle(self.community)

    def next_player(self):
        """
        Sets the current_player to the next
        """
        self.current_player = (self.current_player + 1) % len(self.players)

    def move_player(self, move):
        """
        Moves a player on the board
        :param move: `Move` object, the move of the player
        """
        pass

    def get_player_postition(self, player):
        """
        Gets the position of a given player
        :param player: player whose position needs to be returned
        """
        pass


def validate_arguments(position, owned_by, houses, mortgaged):
    if owned_by is None and houses != 0:
        raise NoOwnerAndHousesException(
            "Tile {} has owner {}, yet there are {} houses."
            .format(position, owned_by, houses))
    if houses != 0 and mortgaged:
        raise HousesYetMortgagedException(
            "Tile {} has {} houses yet is mortgaged"
            .format(position, houses)
        )


# Tiles maps the unique positions to a colour (the numbers) or something
# unique (the strings)
TILES = {
    0: "Go",
    1: 0,
    2: "Community",
    3: 0,
    4: "Tax ",

}


class Tile(object):
    def __init__(self, position, owned_by, houses, mortgaged):
        validate_arguments(position, owned_by, houses, mortgaged)
        self.position = position
        self.colour = 0
        self.price = 0
        self.owned_by = owned_by
        self.houses = houses
        self.mortgaged = mortgaged


class Move(object):
    """
    This class models a move by a player. It contains information about the
    throw of the player, old and new position, doubles, etc
    """

    def __init__(self, player, board):
        self.player = player
        self.board = board

        self.old_position = board.get_player_position(player)

    def throw(self):
        dice1 = random.randrange(1, 7)
        dice2 = random.randrange(1, 7)
        total = dice1 + dice2
