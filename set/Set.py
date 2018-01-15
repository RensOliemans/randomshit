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
