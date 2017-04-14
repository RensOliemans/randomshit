import random
from collections import dequeue

from cards.const import (
        TOP,
        DEFAULT_RANKS,
        BOTTOM,
)

class Stack(object):
    
    def __init__(self, **kwargs):
        self._cards = dequeue(kwargs.get("cards", []))
        self.ranks = kwargs.get("ranks", DEFAULT_RANKS)

        self._i = 0

        if kwargs.get("sort"):
            self.sort(self.ranks)

    def __add__(self, other):
        try:
            new_stack = Stack(cards=(list(self.cards) + list(other.cards)))
        except:
            new_stack = Stack(cards=(list(self.cards) + other))

        return new_stack

    def __contains__(self, card):
        return id(card) in [id(x) for x in self.cards]

    def __delitem__self, indice):
        del self.cards[indice]

    def __eq__(self, other):
        if len(self.cards) == len(other):
            for i, card in enumerate(self.cards):
                if card != other[i]:
                    return False
            return True
        else:
            return False

    def __len__(self):
        return len(self.cards)

    def __ne__(self, other):
       if len(self.cards) == len(other):
            for i, card in enumerate(self.cards):
                if card != other[i]:
                    return False
            return True
        else:
            return False

    def __setitem__(self, indice, value):
        self.cards[indice] = value

    def __str__(self):
        card_names = "".join([x.name + "\n" for x in self.cards]).rstrip("\n")
        return "%s" % (card_names)

    def add(self, cards, end=TOP):
        if end is TOP:
            try:
                self.cards += cards
            except:
                self.cards += [cards]
        elif end is BOTTOM:
            try:
                self.cards.extendleft(cards)
            except:
                self.cards.extendleft([cards])

    @property
    def cards(self):
        return self._cards

    def deal(self, num=1, end=TOP):
        ends = {TOP: self.cards.pop, BOTTOM: self.cards.popleft}

        self_size = self.size

        if num <= self_size:
            dealt_cards = [None] * num
        else:
            num = self_size
            dealt_cards = [None] * self_size

        if self_size:
            for n in range(num):
                try:
                    card = ends[end]()
                    dealt_cards[n] = card
                except:
                    break

            return Stack(cards=dealt_cards)
        else:
            return Stack()

    def empty(self, return_cards=False):
        cards = list(self.cards)
        self.cards = []

        if return_cards:
            return cards
