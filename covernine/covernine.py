import random
import time
import sys

ALGORITHM = None


def game(rounds=1):
    if ALGORITHM is None:
        print("Initialize algorithm first")
        return
    total_sum = 0
    finished = 0
    start_time = time.time()
    for n in range(rounds):
        board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        game_over = False
        while not game_over:
            dice1 = random.randrange(1, 7)
            dice2 = random.randrange(1, 7)
            total = dice1 + dice2
            # print("Total: " + str(total))
            # print("Board: " + str(board))
            result = ALGORITHM(board, total)
            if result == -1:
                points = sum(board)
                if points == 0:
                    finished += 1
                    total_sum -= 10
                    # -10 points or 0?
                else:
                    total_sum += points
                game_over = True
    print("Average score: {} (total: {}, {} rounds).\nIt took {} seconds.\n"
          "Amount of finished games: {}. Percent of finished: {:.2f}%"
          .format(total_sum / rounds, total_sum, rounds,
                  time.time() - start_time, finished,
                  (finished / rounds) * 100))


def highest_first_pop(board, throw):
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


def highest_last_pop(board, throw):
    for i in range(len(board)):
        for j in range(len(board)):
            other_elem = board[j]
            if board[i] != other_elem:
                if board[i] + other_elem == throw:
                    board.pop(i)
                    board.pop(board.index(other_elem))
                    return board
    if throw in board:
        board.pop(board.index(throw))
        return board
    return -1


def closest_first_pop(board, throw):
    if throw in board:
        board.pop(board.index(throw))
        return board
    min_diff = 100
    for elem in board:
        for other_elem in board:
            if elem != other_elem and elem + other_elem == throw:
                diff = abs(elem - other_elem)
                if diff < min_diff:
                    min_diff = diff
    for elem in board:
        for other_elem in board:
            if (abs(elem - other_elem) == min_diff and
                    elem + other_elem == throw):
                board.pop(board.index(elem))
                board.pop(board.index(other_elem))
                return board
    return -1


def closest_last_pop(board, throw):
    min_diff = 100
    for elem in board:
        for other_elem in board:
            if elem != other_elem and elem + other_elem == throw:
                diff = abs(elem - other_elem)
                if diff < min_diff:
                    min_diff = diff
    for elem in board:
        for other_elem in board:
            if (abs(elem - other_elem) == min_diff and
                    elem + other_elem == throw):
                board.pop(board.index(elem))
                board.pop(board.index(other_elem))
                return board
    if throw in board:
        board.pop(board.index(throw))
        return board
    return -1


def random_first_pop(board, throw):
    if throw in board:
        board.pop(board.index(throw))
        return board

    possible = False
    for elem in board:
        for other_elem in board:
            if elem != other_elem and elem + other_elem == throw:
                possible = True
    if possible:
        while True:
            i = random.randrange(1, len(board))
            elem = board[i]
            for other_elem in board:
                if elem != other_elem and elem + other_elem == throw:
                    board.pop(board.index(elem))
                    board.pop(board.index(other_elem))
                    return board
    return -1


def random_last_pop(board, throw):
    possible = False
    for elem in board:
        for other_elem in board:
            if elem != other_elem and elem + other_elem == throw:
                possible = True
    if possible:
        while True:
            i = random.randrange(1, len(board))
            elem = board[i]
            for other_elem in board:
                if elem != other_elem and elem + other_elem == throw:
                    board.pop(board.index(elem))
                    board.pop(board.index(other_elem))
                    return board
    if throw in board:
        board.pop(board.index(throw))
        return board
    return -1


if __name__ == "__main__":
    print("Using default method: highest_first_pop.")
    ALGORITHM = highest_first_pop
    input_rounds = True
    if len(sys.argv) > 1:
        try:
            rounds = int(sys.argv[1])
            input_rounds = False
        except:
            input_rounds = True
    if input_rounds:
        rounds = int(input("How many rounds do you want to play? "))
    game(rounds)
