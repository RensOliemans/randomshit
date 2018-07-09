import argparse
import math
from random import random, choice

from numpy.random import normal


def main(home, away, counter=0):
    diff = away - home
    goal_difference = round(normal(loc=diff*2.08, scale=1.0))
    if goal_difference == 0:
        goal_difference += choice([-1, 1, -1, 1, 0])
    goal_base = max(round(abs(-math.log2(random() + 0.7))), 0)
    result = (goal_base + abs(goal_difference) if goal_difference < 0 else goal_base,
              goal_base + abs(goal_difference) if goal_difference > 0 else goal_base)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Football results generator")
    parser.add_argument('-ch', '--chance_home', type=float,
                        help='Chance of home team winning')
    parser.add_argument('-ca', '--chance_away', type=float,
                        help='Chance of away team winning')
    parser.add_argument('-r', '--rounds', type=int,
                        help='Does multiple rounds and returns the average score',
                        default=1)
    args = parser.parse_args()

    total = [0, 0]
    for _ in range(args.rounds):
        result = main(args.chance_home, args.chance_away)
        total[0] = total[0] + result[0]
        total[1] = total[1] + result[1]
    print(f"({total[0] / args.rounds}, {total[1] / args.rounds})")
