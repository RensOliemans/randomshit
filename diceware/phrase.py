import argparse
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
    "--filename", default="composites-nl", help="filename of the diceware list"
)
parser.add_argument("--length", default=6, type=int, help="length of the passphrase")


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


def main(args):
    f = Path(__file__).parent.absolute().joinpath(args.filename)
    words = get_words(f)
    if args.numbers:
        try:
            print(" ".join(words[int(n)] for n in args.numbers))
        except KeyError:
            print("Number does not exist")
    else:
        print(" ".join(generate_pw(words, args.length)))


if __name__ == "__main__":
    main(parser.parse_args())
