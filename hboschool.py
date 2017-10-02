import random
import sys, getopt, os

min_number = 1
max_number = 10

def play():
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

def guess(quick=False, verbose=False, rand=False):
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
                to_guess_number = random.randrange(min(possible_numbers), max(possible_numbers) + 1)
            else:
                to_guess_number = possible_numbers[len(possible_numbers) // 2]
        except IndexError:
            # impossible, incorrect instructions from user, start the guessing process over
            print("Are you sure? I'm starting over")
            possible_numbers = list(range(min_number, max_number + 1))
            to_guess_number = possible_numbers[len(possible_numbers) // 2]
        if quick:
            if number < to_guess_number:
                counts += 1
                if verbose: print("The AI guessed {}".format(to_guess_number))
                possible_numbers = list(range(min(possible_numbers), to_guess_number))
            elif number > to_guess_number:
                counts += 1
                if verbose: print("The AI guessed {}".format(to_guess_number))
                possible_numbers = list(range(to_guess_number + 1, max(possible_numbers) + 1))
            elif number == to_guess_number:
                counts += 1
                correct = True
                if verbose: print("The AI guessed {}".format(to_guess_number))
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


def main(argv):
    global min_number, max_number
    program_file = os.path.basename(__file__)
    usage_string = "Usage: python3 {} -i <min_number> -a <max_number> (-rpgqv)".format(program_file)
    help_string = usage_string + "\n" + \
                  "-p = disable the play game (human plays)\n" + \
                  "-g = disable the guess game (AI plays)\n" + \
                  "-q = the guess game goes quickly\n" + \
                  "-r = the AI uses random numbers instead of binsearch\n" + \
                  "-v = the program prints the AI guesses\n" + \
                  "-h = show this help menu"
    try:
        opts, args = getopt.getopt(argv, "rpgqhvi:a:", ["min=", "max="])
    except getopt.GetoptError as e:
        print(usage_string)
        sys.exit(2)

    # set min and max numbers
    quick = False
    to_play = True
    to_guess = True
    verbose = False
    rand = False
    for opt, arg in opts:
        if opt == "-h":
            print(help_string)
            sys.exit()
        elif opt in ("-i", "--min"):
            min_number = int(arg)
        elif opt in ("-a", "--max"):
            max_number = int(arg)
        elif opt == "-q":
            quick = True
        elif opt == "-p":
            to_play = False
        elif opt == "-g":
            to_guess = False
        elif opt == "-v":
            verbose = True
        elif opt == "-r":
            rand = True
    if to_play: play()
    if to_guess: guess(quick=quick, verbose=verbose, rand=rand)


if __name__ == "__main__":
    main(sys.argv[1:])
