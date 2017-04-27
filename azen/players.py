import random
import sys, traceback


class Player(object):
    """
    Superclass Player. This class is the main class for a user or AI that
    wishes to play the 'Azen' game
    """

    def __init__(self, username, ui):
        self.username = username
        self.end_score = 0
        self.ui = ui

    def __str__(self):
        return "Username: {0}".format(self.username)

    def __repr__(self):
        return "{0} object with username {1}".format("Player",
                                                     self.username)

    def make_move(self, board, verbose, set_move=True):
        if verbose >= 3:
            self.ui.show_board(board)
        field = board.field
        for i in range(len(field)):
            if len(field[i]) != 0:
                first_card = field[i][-1]
                for j in range(len(field)):
                    if i != j and len(field[j]) != 0:
                        other_card = field[j][-1]
                        if first_card.suit == other_card.suit:
                            if first_card > other_card:
                                if verbose >= 3:
                                    print("Removing {0} with {1}"
                                          .format(other_card, first_card))
                                board.remove_card_location(j, i)
                                # Make a change, so start looking again
                                return self.make_move(board, verbose)
                            else:
                                if verbose >= 3:
                                    print("Removing {0} with {1}"
                                          .format(first_card, other_card))
                                board.remove_card_location(i, j)
                                # Make a change, so start looking again
                                return self.make_move(board, verbose)
        # No changes made (otherwise it would have returned) so return "next"
        if verbose >= 3 and len(board.deck.cards) > 0:
            print("New cards")
        return "next"

    def make_move_with_swap(self, board, verbose, set_move=True):
        attempt_swap = False
        field = board.field
        if verbose >= 3:
            self.ui.show_board(board)
        for i in range(len(field)):
            if len(field[i]) != 0:
                first_card = field[i][-1]
                for j in range(len(field)):
                    if i != j:
                        if len(field[j]) != 0:
                            other_card = field[j][-1]
                            if first_card.suit == other_card.suit:
                                if first_card > other_card:
                                    if verbose >= 3:
                                        print("Removing {0} using {1}"
                                              .format(other_card, first_card))
                                    board.remove_card_location(j, i)
                                    return self.make_move_with_swap(board,
                                                                    verbose)
                                else:
                                    if verbose >= 3:
                                        print("Removing {0} using {1}"
                                              .format(first_card, other_card))
                                    board.remove_card_location(i, j)
                                    return self.make_move_with_swap(board,
                                                                    verbose)
                        else:
                            attempt_swap = True
            else:
                attempt_swap = True
        if attempt_swap:
            self.swap(board, verbose)
        if verbose >= 3:
            print("New cards")
        return "next"


class HumanPlayer(Player):
    """
    Subclass of the Player class, the HumanPlayer class.
    This is, as the name suggests, a class for a Human Player
    """
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        move = self.ui.ask_for_move(board)
        if move[0] == "move":
            location_of_first_card = move[1]
            location_of_empty_stack = move[2]
            board.move_card(location_of_first_card, location_of_empty_stack)
        elif move[0] == "remove":
            location_of_low_card = move[1]
            location_of_high_card = move[2]
            board.remove_card_location(location_of_low_card,
                                       location_of_high_card)
        elif move == "next":
            return "next"

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class NaivePlayer(Player):
    """
    Sublass of the Player class, the NaivePlayer class.
    This is the most simple AI. It checks if there are possible moves, and if
    so, it sets them. If not, it requests new cards.
    """
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        return super().make_move(board, verbose)

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class MovingLargestPlayer(Player):
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move_with_swap(self, board, verbose):
        return super().make_move_with_swap(board, verbose)

    def swap(self, board, verbose):
        field = board.field
        filled_field = {i: field[i] for i in field if len(field[i]) > 1}
        try:
            index = max(filled_field.keys(),
                        key=lambda key: filled_field[key][0])
        except:
            return
        for i in range(len(field)):
            if len(field[i]) == 0:
                if verbose >= 3:
                    self.ui.show_board(board)
                    print("Index of card to swap: {0}, place to swap: {1}"
                          .format(index, i))
                board.move_card(index, i)
                return

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class MovingRandomPlayer(Player):
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        return super().make_move_with_swap(board, verbose)

    def swap(self, board, verbose):
        field = board.field
        filled_field = {i: field[i] for i in field if len(field[i]) > 1}
        try:
            number = random.randrange(1, len(filled_field))
            index = list(filled_field)[number]
        except:
            return
        for i in range(len(field)):
            if len(field[i]) == 0:
                if verbose >= 3:
                    self.ui.show_board(board)
                    print("Index of card to swap: {0}, place to swap: {1}"
                          .format(index, i))
                board.move_card(index, i)
                return

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class MovingSmallestPlayer(Player):
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        return super().make_move_with_swap(board, verbose)

    def swap(self, board, verbose):
        field = board.field
        filled_field = {i: field[i] for i in field if len(field[i]) > 1}
        try:
            index = min(filled_field.keys(),
                        key=lambda key: filled_field[key][0])
        except:
            return
        for i in range(len(field)):
            if len(field[i]) == 0:
                if verbose >= 3:
                    self.ui.show_board(board)
                    print("Index of card to swap: {0}, place to swap: {1}"
                          .format(index, i))
                board.move_card(index, i)
                return

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


class SmarterMovingPlayer(Player):
    def __init__(self, username, ui):
        Player.__init__(self, username, ui)

    def make_move(self, board, verbose):
        return super().make_move_with_swap(board, verbose, set_move=False)

    def swap(self, board, verbose):
        field = board.field
        filled_field = {i: field[i] for i in field if len(field[i]) > 1}
        try:
            best_result, best_index = 0, list(filled_field)[0]
            for i in range(len(filled_field)):
                test_index = list(filled_field)[i]
                result = self.test_swap(board, test_index, verbose)
                if result > best_result:
                    best_result, best_index = result, test_index

            print("{0}, {1}".format(best_result, best_index))
        except:
            # board is empty so list(filled_field)[0] is out of range
            return
        for i in range(len(field)):
            if len(field[i]) == 0:
                if verbose >= 3:
                    self.ui.show_board(board)
                    print("Index of card to swap: {0}, place to swap: {1}"
                          .format(best_index, i))
                board.move_card(best_index, i)
                return

    def test_swap(self, board, test_index, verbose, amount=0):
        """
        Tests how good a swap is.

        :arg test_index
            Index of card to move
        :returns:
            tuple: result (cards removed because of swap)
        """
        print("now in here")
        field = board.field
        for i in range(len(field)):
            if len(field[i]) == 0:
                amount = self.test_move(board, test_index, i, verbose,
                                        board.field, amount)
                print("a" + str(amount))

        return amount

    def test_move(self, board, index_to_move, empty_slot, verbose,
                  custom_field, amount):
        """
        This method tests a removal. It first swaps a move and then
        checks how many cards it can remove afterwards. It returns the
        amount of cards it can remove with the given swap
        """
        if board.check_validity_move(index_to_move, empty_slot):
            first_card = custom_field[index_to_move][-1]
            del custom_field[index_to_move][-1]
            custom_field[empty_slot].append(first_card)

        attempt_swap = False
        for i in range(len(custom_field)):
            if len(custom_field[i]) != 0:
                first_card = custom_field[i][-1]
                for j in range(len(custom_field)):
                    if i != j:
                        if len(custom_field[j]) != 0:
                            other_card = custom_field[j][-1]
                            if first_card.suit == other_card.suit:
                                if first_card > other_card:
                                    if self.valid_remove(j, i, board,
                                                         custom_field):
                                        del custom_field[j][-1]
                                        amount += 1
                                        return self.test_move(board,
                                                              index_to_move,
                                                              empty_slot,
                                                              verbose,
                                                              custom_field)
                                else:
                                    if self.valid_remove(i, j, board,
                                                         custom_field):
                                        del custom_field[i][-1]
                                        amount += 1
                                        return self.test_move(board,
                                                              index_to_move,
                                                              empty_slot,
                                                              verbose,
                                                              custom_field)
                        else:
                            attempt_swap = True
                else:
                    attempt_swap = True
        if attempt_swap:
            filled_field = {i: custom_field[i] for i in
                            custom_field if len(custom_field[i]) > 1}
            try:
                print("in here")
                best_result = amount
                for i in range(len(filled_field)):
                    test_index = list(filled_field)[i]
                    result = self.test_swap(board, test_index, verbose, amount)
                    print(result)
                    if result > best_result:
                        best_result = result
            except:
                return best_result

        return amount

    def valid_remove(self, location_of_low_card,
                     location_of_high_card, board, field):
        try:
            low_card = field[location_of_low_card][-1]
            high_card = field[location_of_high_card][-1]
            return not (location_of_low_card == location_of_high_card
                        or len(field[location_of_low_card]) == 0
                        or len(field[location_of_high_card]) == 0
                        or location_of_low_card >= board.stacks
                        or location_of_high_card >= board.stacks
                        or high_card.suit != low_card.suit
                        or high_card < low_card)
        except KeyError:
            return False

    def invalid_move(self, board, verbose):
        self.ui.show_invalid_move(board)


algorithms = {
    0: HumanPlayer,
    1: NaivePlayer,
    2: MovingLargestPlayer,
    3: MovingRandomPlayer,
    4: MovingSmallestPlayer,
    5: SmarterMovingPlayer,
}


def parse(message):
    for i in range(len(algorithms)):
        if message == str(i):
            return algorithms[i]
    raise ValueError("Wrong algorithm number.")
