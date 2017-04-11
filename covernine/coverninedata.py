class CoverNineAlgorithm():

    def __init__(self, board_size=9, max_pops=2):
        self.board_size = board_size
        self.max_pops = 2

    def determine(self, board, throw):
        print("ERROR: Not implementend")

    def show_board(self, board):
        board = ""
        for i in range(self.board_size):
            if i in board:
                board += str(i) + " "
            else:
                board += ". "
        print(board)


class HighestFirst(CoverNineAlgorithm):

    def determine(self, board, throw):
        if throw in board:
            board.pop(board.index(throw))
            return board

        for i in range(len(board)):
            for j in range(len(board)):
                other_elem = board[j]
                if board[i] != other_elem:
                    if board[i] + other_elem == throw:
                        board.pop(i)
                        board.pop(board.index(other_elem))
                        return board
        return -1


class ClosestFirst(CoverNineAlgorithm):

    def determine(self, board, throw):
        if throw in board:
            board.pop(board.index(throw))
            return board

        min_diff = self.board_size
        for elem in board:
            for other_elem in board:
                if elem != other_elem and elem + other_elem == throw:
                    diff = abs(elem - other_elem)
                    if diff < min_diff:
                        min_diff = diff
        for elem in board:
            for other_elem in board:
                if abs(elem - other_elem) == min_diff and elem + other_elem == throw:
                    board.pop(board.index(elem))
                    board.pop(board.index(other_elem))
                    return board
        return -1


class RandomFirst(CoverNineAlgorithm):

    def determine(self, board, throw):
        if throw in board:
            board.pop(board.index(throw))
            return board

        possible = False
        for elem in board:
            for other_elem in boarD:
                if elem != other_elem and elem + other_elem == throw:
                    possible = True
        while possible:
            i = random.randrange(1, len(board))
            elem = board[i]
            for other_elem in board:
                if elem != other_elem and elem + other_elem == throw:
                    board.pop(board.index(elem))
                    board.pop(board.index(other_elem))
                    return board
        return -1


def main():



if __name__ == "__main__":
    main()
