import argparse

from gebouw import Gebouw, Kunst

parser = argparse.ArgumentParser(description='Pak alle gebouwen (en kunstwerken) op de UT.')
parser.add_argument('-l', '--letters', type=str,
                    help='welke letters heeft het gebouw?')
args = parser.parse_args()


def parse_new():
    with open('buildings') as f:
        lines = f.read()
    lines = lines.split('\n')[1:-1]
    gebouwen = list()
    for line in lines:
        items = line.split('\t')
        gebouwen.append(Gebouw(nummer=int(items[0]), naam=items[1], afkorting=items[2]))

    with open('kunst') as f:
        lines = f.read()
    lines = lines.split('\n')[1:-1]
    kunstwerken = list()
    for line in lines:
        items = line.split('\t')
        kunstwerken.append(Kunst(naam=items[0]))

    return gebouwen, kunstwerken


gebouwen, kunstwerken = parse_new()
print([x for x in gebouwen if all([l in x.naam.lower() for l in args.letters.lower()])])
