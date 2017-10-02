import random
import sys, getopt, os

min_number = 1
max_number = 10

def play():
    number = random.randrange(min_number, max_number + 1)
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
    # make sure number is between min_number and max_number
    while number < min_number or number > max_number:
        number = int(input("What's the number the AI should guess? "))
    possible_numbers = list(range(min_number, max_number + 1))
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
            possible_numbers = list(range(min_number, max_number + 1))
            to_guess_number = possible_numbers[len(possible_numbers) // 2]
        answer = input("The AI guessed {}. Say 'lower', 'higher', or 'yes' ".format(to_guess_number))
        if answer.lower() == "lower":
            possible_numbers = list(range(min(possible_numbers), to_guess_number))
        elif answer.lower() == "higher":
            possible_numbers = list(range(to_guess_number + 1, max(possible_numbers) + 1))
        elif answer.lower() == "yes":
            correct = True
        # if another instruction is used, nothing changes, so the AI asks the same number


def main(argv):
    global min_number, max_number
    program_file = os.path.basename(__file__)
    usage_string = "{} -i <min_number> -a <max_number>".format(program_file)
    try:
        opts, args = getopt.getopt(argv, "hi:a:", ["min=", "max="])
    except getopt.GetoptError as e:
        print(usage_string)
        sys.exit(2)

    # set min and max numbers
    for opt, arg in opts:
        if opt == "-h":
            print(usage_string)
            sys.exit()
        elif opt in ("-i", "--min"):
            min_number = int(arg)
        elif opt in ("-a", "--max"):
            max_number = int(arg)
    play()
    guess()


if __name__ == "__main__":
    main(sys.argv[1:])
