from cards.deck import Deck

deck = Deck()
deck.shuffle()
board = dict()  # key index, value list of cards

board[0] = deck.deal(1)
board[1] = deck.deal(1)
board[2] = deck.deal(1)
board[3] = deck.deal(1)

# while len(deck) != 0:
print(board)
for stack in board:
    top_card = board[stack][len(board[stack]) - 1]
    for other_stack in board:
        other_top_card = board[other_stack][len(board[other_stack]) - 1]
        if stack != other_stack and top_card.suit == other_top_card.suit:
            if top_card.value > other_top_card.value:
                # How to remove card from stack?
                board[stack].remove(top_card)
            else:
                board[other_stack].remove(other_top_card)

board[0] += deck.deal(1)
board[1] += deck.deal(1)
board[2] += deck.deal(1)
board[3] += deck.deal(1)
