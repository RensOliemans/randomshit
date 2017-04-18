# ============================================================================
# Cards - Tools
# ---------------------------------------------------------------------------
# Version: 0.1
# Updated: 14-04-2017
# Author: Rens Oliemans
# Note: Derived from PyDealer module
# ============================================================================

"""
The tools module contains functions for working with sequences of cards, some
of which are used by the classes in the Cards package, such as the functions
``build_cards``, ``sort_cards``, and ``check_term``, for example.
"""

# ============================================================================
# Imports
# ============================================================================

import random
import time

from cards.card import Card
from cards.const import (
    DEFAULT_RANKS,
    VALUES,
    SUITS,
)


# ============================================================================
# Utility Functions
# ============================================================================

def build_cards(jokers=False, num_jokers=0):
    """
    Builds a list containing a full French deck of 52 Card instances. The
    cards are sorted according to ``DEFAULT_RANKS``.

    :arg bool jokers:
        Whether or not to incllude jokers in the deck.
    :arg int num_jokers:
        The number of jokers to include.

    :returns:
        A list containing a full French deck of 52 Card instances.
    """
    new_deck = []

    if jokers:
        new_deck += [Card("Joker", None) for i in range(num_jokers)]

    new_deck += [Card(value, suit) for value in VALUES for suit in SUITS]

    return new_deck


def check_sorted(cards, ranks=None):
    """
    Checks whether the given cards are sorted by the given ranks.

    :arg cards:
        The cards to check. Can be a ``Stack``, ``Deck``, or ``list`` of
        ``Card`` instances.
    :arg dict_ranks:
        The ranks to check against. Default is DEFAULT_RANKS.

    :returns:
        ``True`` or ``False``.
    """
    ranks = ranks or DEFAULT_RANKS

    sorted_cards = sort_cards(cards, ranks)

    if cards[::-1] == sorted_cards:
        print("Inverted is sorted")
    return cards == sorted_cards or cards[::-1] == sorted_cards


def check_term(card, term):
    """
    Checks a given search term against a given card's ful name, suit,
    value, and abbreviation.

    :arg Card card:
        The card to check.
    :arg str term:
        The search term to check for. Can be a card full name, suit,
        value, or abbreviation.

    :returns:
        ``True`` or ``False``.
    """
    check_list = [
        x.lower() for x in [card.name, card.suit, card.value, card.abbrev,
                            card.suit[0], card.value[0]]
    ]

    term = term.lower()

    for check in check_list:
        if check == term:
            return True
    return False


def compare_stacks(cards_x, cards_y, sorted=False):
    """
    Checks whether two given ``Stack``, ``Deck``, or ``list`` instances
    contain the same cards (based on value & suit, not instance). Does not
    take into account the ordering.

    :arg cards_x:
        The first stack to check. Can be a ``Stack``, ``Deck``, or ``list``
        instance.
    :arg cards_y:
        The second stack to check. Can be a ``Stack``, ``Deck``, or ``list``
        instance.
    :arg bool sorted:
        Whether or not the cards are already sorted. If ``True``, then
        ``compare_stacks`` will skip the sorting process.

    :returns:
        ``True`` or ``False``.
    """
    if len(cards_x) == len(cards_y):
        if not sorted:
            cards_x = sort_cards(cards_x, DEFAULT_RANKS)
            cards_y = sort_cards(cards_y, DEFAULT_RANKS)
        for i, c in enumerate(cards_x):
            if c != cards_y[i]:
                return False
        return True
    else:
        return False


def find_card(cards, term, limit=0, sort=False, ranks=None):
    """
    Searches the stack for cards with a value, suit, name, or abbreviation
    matching the given argument, 'term'.
    :arg str term:
        The search term. Can be a card full name, value, suit, or
        abbreviation.
    :arg int limit:
        The number of items to retrieve for each term. ``0`` equals
        no limit.
        Defaults to 0
    :arg bool sort:
        Whether or not to sort the results.
        Defaults to False
    :arg dict ranks:
        The rank dict to reference for sorting. It ``None``, it will
        default to ``DEFAULT_RANKS``.
    :returns:
        A list of stack indices for the cards matching the given terms,
        if found.
    """
    found_indices = []
    count = 0
    if not limit:
        for i, card in enumerate(cards):
            if check_term(card, term):
                found_indices.append(i)
    else:
        for i, card in enumerate(cards):
            if count < limit:
                if check_term(card, term):
                    found_indices.append(i)
                    count += 1
            else:
                break
    if sort:
        found_indices = sort_card_indices(found_indices, ranks)
    return found_indices


def find_list(cards, terms, limit=0, sort=False, ranks=None):
    """
    Searches the stack for cards with a value, suit, name, or abbreviation
    matching the given argument, 'term'.
    :arg list terms:
        The search terms. Can be card full names, suits, values,
        or abbreviations.
    :arg int limit:
        The number of items to retrieve for each term.
    :arg bool sort:
        Whether or not to sort the results.
        Defaults to False
    :arg dict ranks:
        The rank dict to reference for sorting. It ``None``, it will
        default to ``DEFAULT_RANKS``.
    :returns:
        A list of stack indices for the cards matching the given terms,
        if found.
    """
    found_indices = []
    count = 0

    if not limit:
        for term in terms:
            for i, card in enumerate(cards):
                if check_term(card, term) and i not in found_indices:
                    found_indices.append(i)
    else:
        for term in terms:
            for i, card in enumerate(cards):
                if count < limit:
                    if check_term(card, term) and i not in found_indices:
                        found_indices.append(i)
                        count += 1
                else:
                    break
            count = 0

    if sort:
        found_indices = sort_card_indices(cards, found_indices, ranks)

    return found_indices


def get_card(cards, term, limit=0, sort=False, ranks=None):
    """
    Get the specified card from the stack.

    :arg cards:
        The cards to get from. Can be a ``Stack``, ``Deck`` or ``list``
        of card instances.
    :arg str term:
        the card's full name, value, suit, abbreviation, or stack indice.
    :arg int limit:
        The number of items to retrieve for each term.
    :arg bool sort:
        Whether or not to sort the results.
    :arg dict ranks:
        If ``sort=True``, the rank dict to refer to for sorting.

    :returns:
        A copy of the given cards, with the found cards removed, and a list
        of the specified cards, if found.
    """
    got_cards = []

    try:
        indices = find_card(cards, term, limit=limit)
        got_cards = [cards[i] for i in indices]
        cards = [v for i, v in enumerate(cards) if i not in indices]
    except:
        got_cards = [cards[term]]
        cards = [v for i, v in enumerate(cards) if i is not term]

    if sort:
        got_cards = sort_cards(got_cards)

    return cards, got_cards


def get_list(cards, terms, limit=0, sort=False, ranks=None):
    """
    Get the specified cards from the stack.

    :arg cards:
        The cards to get from. Can be a ``Stack``, ``Deck`` or ``list``
        of card instances.
    :arg str term:
        A list of card's full names, values, suits, abbreviations, or stack
        indices.
    :arg int limit:
        The number of items to retrieve for each term.
    :arg bool sort:
        Whether or not to sort the results.
    :arg dict ranks:
        If ``sort=True``, the rank dict to refer to for sorting.

    :returns:
        A list of the specified cards, if found.
    """
    got_cards = []

    try:
        indices = find_list(cards, terms, limit=limit)
        got_cards = [cards[i] for i in indices if cards[i] not in got_cards]
        cards = [v for i, v in enumerate(cards) if i not in indices]
    except:
        indices = []
        for item in terms:
            try:
                card = cards[item]
                if card not in got_cards:
                    got_cards.append(card)
                    indices.append(item)
            except:
                indices += find_card(cards, item, limit=limit)
                got_cards += [card[i] for i in indices
                              if cards[i] not in got_cards]
        cards = [v for i, v in enumerate(cards) if i not in indices]

    if sort:
        got_cards = sort_cards(got_cards, ranks)

    return cards, got_cards


def open_cards(filename=None):
    """
    To implement.
    """
    pass


def random_card(cards, remove=False):
    """
    Returns a random card from the Stack. If ``remove=True``, it will
    also remove the card from the deck.

    :arg bool remove:
        Whether or not to remove the card from the deck.

    :return:
        A random Card object, from the stack
    """
    if not remove:
        return random.choice(cards)
    else:
        i = random.randrange(len(cards))
        card = cards[i]
        del cards[i]
        return card


def save_cards(cards, filename=None):
    """
    To implement.
    """
    pass


def sort_card_indices(cards, indices, ranks=None):
    """
    Sorts the given Deck indices by the given ranks. Must also supply the
    ``Stack``, ``Deck``, or ``list`` that the indices are from.

    :arg cards:
        The cards the indices are from. Can be a ``Stack``, ``Deck``, or 
        ``list`` of card instances.
    :arg list indices:
        The indices to sort.
    :arg dict ranks:
        The rank dict to reference for sorting. If ``Non``, it will
        default to ``DEFAULT_RANKS``.

    :returns:
        The sorted indices.
    """
    ranks = ranks or DEFAULT_RANKS

    if ranks.get("suits"):
        indices = sorted(
                indices,
                key=None
        )
