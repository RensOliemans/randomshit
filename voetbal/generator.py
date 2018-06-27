# from random import randint
import argparse

from numpy.random import choice

parser = argparse.ArgumentParser(description="Football results generator")
parser.add_argument('-ch', '--chance_home', type=float,
                    help='Chance of home team winning')
parser.add_argument('-cd', '--chance_draw', type=float,
                    help='Chance of a draw')
parser.add_argument('-ho', '--home', type=str,
                    help='Name of home team', default='Home')
parser.add_argument('-a', '--away', type=str,
                    help='Name of away team', default='Away')
args = parser.parse_args()

try:
    chance_away = 1 - sum((args.chance_home, args.chance_draw))
    result = choice((args.home, 'Draw', args.away), p=(args.chance_home, args.chance_draw, chance_away))
    print(result)
except TypeError:
    parser.print_help()
