import argparse
import math
from random import random, choice

from numpy.random import normal


def main(home, away, counter=0):
    diff = away - home
    goal_difference = round(normal(loc=diff*2.08, scale=0))
    if goal_difference == 0:
        goal_difference += choice([-1, 1])
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
    args = parser.parse_args()

    result = main(args.chance_home, args.chance_away)
    print(result)
