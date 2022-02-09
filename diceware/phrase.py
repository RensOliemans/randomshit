import argparse
import pyperclip
from pathlib import Path
from random import SystemRandom

r = SystemRandom()


parser = argparse.ArgumentParser(description="Create secure passphrases.")
parser.add_argument(
    "numbers",
    metavar="N",
    type=int,
    nargs="*",
    help="numbers to get diceware words from",
)
parser.add_argument(
    "-f", "--filename", default="nl-comp", help="filename of the diceware list"
)
parser.add_argument(
    "-l", "--length", default=6, type=int, help="length of the passphrase"
)
parser.add_argument(
    "-c",
    "--copy",
    default=False,
    action=argparse.BooleanOptionalAction,
    help="Copy the passphrase to the clipboard",
)
parser.add_argument(
    "-s",
    "--show",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="Print the passphrase to stdout",
)
parser.add_argument(
    "-i",
    "--interactive",
    default=False,
    action=argparse.BooleanOptionalAction,
    help="Interactive mode",
)


def get_file(filename):
    file_in_source_dir = (
        Path(__file__).parent.absolute().joinpath("wordlists", filename)
    )
    if file_in_source_dir.exists():
        return file_in_source_dir

    file_in_working_dir = Path(filename).absolute()
    if file_in_working_dir.exists():
        return file_in_working_dir

    raise ValueError(f"No wordlist found with filename '{filename}'")


def get_words(filename):
    with open(filename) as f:
        words = [x.strip().split("\t") for x in f.readlines()]
        return {int(w[0]): w[1] for w in words}


def generate_pw(words, length):
    x = 0
    keys = list(words.keys())
    while x < length:
        number = r.choice(keys)
        yield words[number]
        x += 1


def output_passphrase(passphrase, args):
    if args.show:
        print(passphrase)
    if args.copy:
        pyperclip.copy(passphrase)


def interactive(words):
    number = input(
        "Enter 5-digit numbers as many times as the desired length of your passphrase. "
        "Leave empty to finish.\n"
    )
    while True:
        if number == "":
            return
        try:
            yield words[int(number)]
        except (KeyError, ValueError):
            print("Invalid number.")

        number = input()


def main(args):
    f = get_file(args.filename)
    words = get_words(f)
    if args.interactive:
        output_passphrase(" ".join(interactive(words)), args)
        return

    if args.numbers:
        try:
            output_passphrase(" ".join(words[int(n)] for n in args.numbers), args)
        except KeyError:
            print("Number does not exist")
    else:
        output_passphrase(" ".join(generate_pw(words, args.length)), args)


if __name__ == "__main__":
    main(parser.parse_args())
