import gameobjects
import constants
import players


def game(player1):
    board = gameobjects.Board()

    while board.deck.cards:
        move = player1.move(board)
        if move is None:
            board.extra_cards()
            print("No set can be found, new set")
        else:
            print("Set has been found!")
            player1.cards.extend(move)
            board.remove_cards(move)
    print(len(player1.cards))


def is_set(cards):
    if not len(cards) == constants.GAME_AMOUNT:
        return False

    sames = [x + y for x in cards for y in cards if not x == y]

    return all(sames[0] == item for item in sames)


if __name__ == "__main__":
    player1 = players.NaiveAI()
    game(player1)


"""
def is_set(card1, card2, card3):
    def sames(card1, card2, card3):
        sames_1 = card1 + card2
        sames_2 = card1 + card3
        sames_3 = card2 + card3
        return (sames_1 == sames_2 and sames_2 == sames_3
                and sames_1 == sames_3)

    def diffs(card1, card2, card3):
        diffs_1 = card1 - card2
        diffs_2 = card1 - card3
        diffs_3 = card2 - card3
        return (diffs_1 == diffs_2 and diffs_2 == diffs_3
                and diffs_1 == diffs_3)

    return sames(card1, card2, card3) and diffs(card1, card2, card3)"""
