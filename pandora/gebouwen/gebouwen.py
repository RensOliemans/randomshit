import argparse

from gebouw import Gebouw, Kunst

parser = argparse.ArgumentParser(description='Pak alle gebouwen (en kunstwerken) op de UT.')
parser.add_argument('-l', '--letters', type=str,
                    help='welke letters heeft het gebouw? (ergens in de naam)')
parser.add_argument('-a', '--aantal', type=int,
                    help='hoeveel letters heeft het gebouw?')
parser.add_argument('-b', '--begin', type=str,
                    help='wat zijn de eerste letters van het gebouw?')
parser.add_argument('-e', '--eind', type=str,
                    help='wat zijn de laatste letters van het gebouw?')
parser.add_argument('-m', '--midden', type=str,
                    help='gebruik: [<index><letter> ]+')
parser.add_argument('-k', '--kunst', dest='kunst', action='store_true',
                    help='neem de kunstwerken ook mee')
args = parser.parse_args()


def parse_new():
    with open('buildings.txt') as f:
        lines = f.read()
    lines = lines.split('\n')[1:-1]
    gebouwen = list()
    for line in lines:
        items = line.split('\t')
        gebouwen.append(Gebouw(number=int(items[0]), name=items[1], abbreviation=items[2]))

    with open('kunst.txt') as f:
        lines = f.read()
    lines = lines.split('\n')[1:-1]
    kunstwerken = list()
    for line in lines:
        items = line.split('\t')
        kunstwerken.append(Kunst(name=items[0]))

    return gebouwen, kunstwerken

gebouwen, kunstwerken = parse_new()
total = gebouwen + kunstwerken
check = total if args.kunst else gebouwen


if args.begin:
    check = [x for x in check if x.name.lower()[:len(args.begin)] == args.begin.lower()]
if args.midden:
    indices = {int(x[0]): x[1] for x in args.midden.split(' ')}
    check = [x for x in check if all(x.name.lower()[min(len(x) - 1, p)] == indices[p] for p in indices.keys())]
if args.eind:
    check = [x for x in check if x.name.lower()[-len(letters):] == letters.lower()]
if args.letters:
    check = [x for x in check if all([l in x.name.lower() for l in args.letters.lower()])]
if args.aantal:
    check = [x for x in check if len(x.name) == args.aantal]
print(check)
