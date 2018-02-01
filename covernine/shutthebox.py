import random
import time


def game(rounds=1):
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
            print("Throw: " + str(total))
            # print("Board: " + str(board))
            result = highest_first_pop(board, total)
            if result == -1:
                points = sum(board)
                if points == 0:
                    finished += 1
                    total_sum -= 10
                else:
                    total_sum += points
                game_over = True
    print("Average score: {} (total: {}, {} rounds. It took {} seconds."
          .format(total_sum / rounds, total_sum, rounds,
                  time.time() - start_time))
    print(finished)


def highest_first_pop(board, throw):
    if throw in board:
        board.pop(board.index(throw))
        print("Removing " + str(throw))
        return board
    # holy shit what was i thinking here wtf
    for i in range(len(board)):
        for j in range(len(board)):
            for k in range(len(board)):
                for m in range(len(board)):
                    indices = [board[i], board[j], board[k], board[m]]
                    if len(set(indices)) == len(indices):
                        if board[i] + board[j] == throw:
                            other_elem = board[j]
                            print("Removing " + str(board[i]) + " and " + str(other_elem))
                            board.pop(i)
                            board.pop(board.index(other_elem))
                            return board
                        if board[i] + board[j] + board[k] == throw:
                            elem_two = board[j]
                            elem_three = board[k]
                            print("Removing " + str(board[i]) + " and " + str(elem_two) +
                                  " and " + str(elem_three))
                            board.pop(i)
                            board.pop(board.index(elem_two))
                            board.pop(board.index(elem_three))
                            return board
                        if board[i] + board[j] + board[k] + board[m] == throw:
                            elem_two = board[j]
                            elem_three = board[k]
                            elem_four = board[m]
                            print("Removing " + str(board[i]) + " and " + str(elem_two) +
                                  " and " + str(elem_three) + " and " + str(elem_four))
                            board.pop(i)
                            board.pop(board.index(elem_two))
                            board.pop(board.index(elem_three))
                            board.pop(board.index(elem_four))
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
            if abs(elem - other_elem) == min_diff and elem + other_elem == throw:
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
            if abs(elem - other_elem) == min_diff and elem + other_elem == throw:
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
