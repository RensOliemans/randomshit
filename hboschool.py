import random

MIN_NUMBER = 1
MAX_NUMBER = 100

def play():
    number = random.randrange(MIN_NUMBER, MAX_NUMBER + 1)
    guessed = False
    while not guessed:
        guess = int(input("Number? "))
        if guess < number:
            print("Hoger")
        elif guess > number:
            print("Lager")
        elif guess == number:
            guessed = True
            print("Correct!")

def guess():
    number = -1
    # make sure number is between 1 and 10
    while number < MIN_NUMBER or number > MAX_NUMBER:
        number = int(input("What's the number the AI should guess? "))
    possible_numbers = list(range(MIN_NUMBER, MAX_NUMBER + 1))
    correct = False
    while not correct:
        try:
            # uncomment next line so AI chooses a number at random
            # to_guess_number = random.randrange(min(possible_numbers), max(possible_numbers) + 1)
            # uncomment next line so AI chooses the middle number in the list
            to_guess_number = possible_numbers[len(possible_numbers) // 2]
        except IndexError:
            # impossible, incorrect instructions from user, start the guessing process over
            print("Are you sure? I'm starting over")
            possible_numbers = list(range(MIN_NUMBER, MAX_NUMBER + 1))
            to_guess_number = possible_numbers[len(possible_numbers) // 2]
        answer = input("The AI guessed {}. Say 'lower', 'higher', or 'yes' ".format(to_guess_number))
        if answer.lower() == "lower":
            possible_numbers = list(range(min(possible_numbers), to_guess_number))
        elif answer.lower() == "higher":
            possible_numbers = list(range(to_guess_number + 1, max(possible_numbers) + 1))
        elif answer.lower() == "yes":
            correct = True
        # if another instruction is used, nothing changes, so the AI asks the same number


if __name__ == "__main__":
    play()
    guess()
