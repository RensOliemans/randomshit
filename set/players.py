# from gameobjects import Board
import Set


class NaiveAI(object):
    def __init__(self):
        self.cards = []

    @classmethod
    def move(cls, board):
        board = board.board
        for c1 in board:
            for c2 in board:
                for c3 in board:
                    if c1 == c2 or c1 == c3 or c2 == c3:
                        continue
                    if Set.is_set((c1, c2, c3)):
                        return (c1, c2, c3)
        return None
