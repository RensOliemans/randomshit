from collections import namedtuple
from gebouw import Gebouw, Kunst


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
