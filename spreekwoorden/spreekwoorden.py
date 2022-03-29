#!/usr/bin/python

import json
import os
import argparse
from random import sample


parser = argparse.ArgumentParser(description="Gets some Dutch proverbs at random.")


def load_proverbs():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    filename = current_dir + "/dump.json"
    proverbs = dict()
    with open(filename) as f:
        proverbs = json.load(f)
    return proverbs


def main(a: "Amount of proverbs" = 5, d: "To define" = True):
    """Gets some Dutch proverbs at random."""
    proverbs = load_proverbs()
    sampled = sample(list(proverbs), min(a, len(proverbs)))
    chosen = [(c, proverbs[c]) for c in sampled]
    if d:
        max_len = max([len(elem[0]) for elem in chosen]) + 4
        print("\n".join(f"{elem[0]:{max_len}}{elem[1]}" for elem in chosen))
    else:
        print("\n".join(choice[0] for choice in chosen))


if __name__ == "__main__":
    parser.add_argument(
        "-a", "--amount", type=int, help="Amount of proverbs", default=5
    )
    parser.add_argument(
        "-nd", "--no-define", action="store_false", help="Don't define", default=True
    )
    args = parser.parse_args()
    main(args.amount, args.no_define)
