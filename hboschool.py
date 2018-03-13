import random
import begin


""" This file is an atrocity """


def play(min_number, max_number):
    counts = 0
    number = random.randrange(min_number, max_number + 1)
    guessed = False
    while not guessed:
        guess = int(input("Number? "))
        if guess < number:
            counts += 1
            print("Hoger")
        elif guess > number:
            counts += 1
            print("Lager")
        elif guess == number:
            guessed = True
            counts += 1
            print("Correct! In {} tries!".format(counts))


def guess(min_number, max_number, quick=False, verbose=False, rand=False):
    number = -1
    # make sure number is between min_number and max_number
    while number < min_number or number > max_number:
        number = int(input("What's the number the AI should guess? "))
    possible_numbers = list(range(min_number, max_number + 1))
    correct = False
    counts = 0
    while not correct:
        try:
            if rand:
                to_guess_number = random.randrange(
                        min(possible_numbers), max(possible_numbers) + 1)
            else:
                to_guess_number = possible_numbers[len(possible_numbers) // 2]
        except IndexError:
            # impossible, incorrect instructions from user, start the guessing
            # process over
            print("Are you sure? I'm starting over")
            possible_numbers = list(range(min_number, max_number + 1))
            to_guess_number = possible_numbers[len(possible_numbers) // 2]
        if quick:
            if number < to_guess_number:
                counts += 1
                if verbose:
                    print("The AI guessed {}".format(to_guess_number))
                possible_numbers = list(range(min(possible_numbers), to_guess_number))
            elif number > to_guess_number:
                counts += 1
                if verbose:
                    print("The AI guessed {}".format(to_guess_number))
                possible_numbers = list(range(to_guess_number + 1, max(possible_numbers) + 1))
            elif number == to_guess_number:
                counts += 1
                correct = True
                if verbose:
                    print("The AI guessed {}".format(to_guess_number))
                print("{} tries".format(counts))
        else:
            answer = input("The AI guessed {}. Say 'lower', 'higher', or 'yes' ".format(to_guess_number))
            if answer.lower() == "lower":
                counts += 1
                possible_numbers = list(range(min(possible_numbers), to_guess_number))
            elif answer.lower() == "higher":
                counts += 1
                possible_numbers = list(range(to_guess_number + 1, max(possible_numbers) + 1))
            elif answer.lower() == "yes":
                counts += 1
                correct = True
                print("{} tries".format(counts))
            # if another instruction is used, nothing changes, so the AI asks the same number


@begin.start(auto_convert=True)
def main(i: 'Min number' = 1, a: 'Max number' = 10,
         p: 'Disable play game (human plays)' = True,
         g: 'Disable guess game (AI plays)' = True,
         q: 'Guess game goes quickly' = False,
         r: 'AI uses random instead of binary search' = False,
         v: 'Verbose' = True):
    """ Guessing game, player and AI can play """
    if p:
        play(i, a)
    if g:
        guess(i, a, quick=q, verbose=v, rand=r)
