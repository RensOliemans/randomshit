from random import sample

NUMBERS_PER_CARD = 5 * 5    # 25 numbers per bingo card
AMOUNT_OF_CARDS = 40


def create_cards(numbers=NUMBERS_PER_CARD, amount=AMOUNT_OF_CARDS):
    cards = []
    while len(cards) < AMOUNT_OF_CARDS:
        card = sample(range(1, 101), k=NUMBERS_PER_CARD)
        if card not in cards:
            cards.append(card)
    return cards


if __name__ == "__main__":
    cards = create_cards()
    print("The cards are:")
    for card in cards:
        print(card)
        card.sort()
    print("\nThe cards, sorted, are:")
    for card in cards:
        print(card)
