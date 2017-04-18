"""
This module contains the ``Card`` class. Each ``Card`` instance represents a 
single playing card, of a given value and suit.
"""

# ============================================================================
# Imports
# ============================================================================

from cards.const import DEFAULT_RANKS


# ============================================================================
# Card Class
# ============================================================================

class Card(object):
    """
    The Card class, each instance representing a single playing card.

    :arg str value:
        The card value.
    :arg str suit:
        The card suit.
    """

    def __init__(self, value, suit):
        """
        Card constructor method.

        :arg str value:
            The card value.
        :arg str suit:
            The card suit.

        """
        self.value = str(value).capitalize()
        self.suit = str(suit).capitalize() if suit else suit
        self.abbrev = card_abbrev(self.value, self.suit)
        self.name = card_name(self.value, self.suit)

    def __eq__(self, other):
        """
        Allows for Card value/suit equality comparison.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.
        """

        return (
            isinstance(other, Card) and self.value == other.value and
            self.suit == other.suit
        )

    def __ne__(self, other):
        """
        Allows for Card value/suit equality comparison.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.
        """
        return (
            isinstance(other, Card) and self.value != other.value or
            self.suit != other.suit
        )

    def __ge__(self, other):
        """
        Allows for Card ranking comparisons. Uses DEFAULT_RANKS for comparison.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.
        """
        if isinstance(other, Card):
            return (
                DEFAULT_RANKS["values"][self.value] >
                DEFAULT_RANKS["values"][other.value] or
                (
                    DEFAULT_RANKS["values"][self.value] >=
                    DEFAULT_RANKS["values"][other.value] and
                    DEFAULT_RANKS["suits"][self.suit] >=
                    DEFAULT_RANKS["suits"][other.suit]
                )
            )
        else:
            return False

    def __gt__(self, other):
        """
        Allows for Card ranking comparisons. Uses DEFAULT_RANKS for comparison.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.
        """
        if isinstance(other, Card):
            return (
                DEFAULT_RANKS["values"][self.value] >
                DEFAULT_RANKS["values"][other.value] or
                (
                    DEFAULT_RANKS["values"][self.value] >=
                    DEFAULT_RANKS["values"][other.value] and
                    DEFAULT_RANKS["suits"][self.suit] >=
                    DEFAULT_RANKS["suits"][other.suit]
                )
            )
        else:
            return False

    def __hash__(self):
        """
        Returns the hash value of the ``Card`` instance.

        :returns:
            A unique number, or has for the Card.

        """
        return hash((self.value, self.suit))

    def __repr__(self):
        """
        Returns a string representation of the ``Card`` instance.

        :returns:
            A string representation of the Card instance.

        """
        return "Card(value={0}, suit={1}".format(self.value, self.suit)

    def __str__(self):
        """
        Returns the full name of the ``Card`` instance.

        :returns:
            The card name.

        """
        return "{}".format(self.name)

    def eq(self, other, ranks=None):
        """
        Allows for Card ranking comparisons. Uses DEFAULT_RANKS for comparison.

        :arg Card other:
            The other card to compare to.

        :returns:
            ``True`` or ``False``.
        """
        ranks = ranks or DEFAULT_RANKS
        if isinstance(other, Card):
            if ranks.get("suits"):
                return (
                    ranks["values"][self.value] ==
                    ranks["values"][other.value] and
                    ranks["suits"][self.suit] ==
                    ranks["suits"][other.suit]
                )
            else:
                return ranks[self.value] == ranks[other.value]
        else:
            return False


# ============================================================================
# Helper Functions
# ============================================================================

def card_abbrev(value, suit):
    """
    Constructs an abbreviation for the card, using the given value and suit.

    :arg str value:
        The value to use.
    :arg str suit:
        The suit to use.

    :returns:
        A newly constructed abbreviation, using the given value and suit.

    """
    if value == "Joker":
        return "JKR"
    elif value == "10":
        return "10{0}".format(suit[0])
    else:
        return "{0}{1}".format(value[0], suit[0])


def card_name(value, suit):
    """
    Constructs a name for the card, using the given value and suit.

    :arg str value:
        The value to use.
    :arg str suit:
        The suit to use.

    :returns:
        A newly constructed name, using the given value and suit.

    """
    if value == "Joker":
        return "Joker"
    else:
        return "{0} of {1}".format(value, suit)
