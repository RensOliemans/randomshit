from pathlib import Path
from random import SystemRandom

import begin

r = SystemRandom()


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


@begin.start(auto_convert=True)
def main(
    n: "Get word of specific number" = None,
    f: "Name of file" = "composites-nl",
    l: "Length of passphrase" = 6,
):
    f = Path(__file__).parent.absolute().joinpath(f)
    words = get_words(f)
    if n:
        try:
            print(words[int(n)])
        except KeyError:
            print("Number does not exist")
    else:
        print(" ".join(generate_pw(words, l)))
