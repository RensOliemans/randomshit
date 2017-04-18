import pydealer

deck = pydealer.Deck()
deck.shuffle()
board = deck.deal(4)
for card in board:
    for other_card in board:
        if not card == other_card and card.suit == other_card.suit:
            if card.value > other_card.value:
                board.
