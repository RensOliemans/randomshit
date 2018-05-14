from collections import namedtuple


def parse2():
    with open('lijst2.txt') as f:
        lines = list(f)

    lines = lines[2:]
    Gebouw = namedtuple('Gebouw', 'nummer naam vertaling uitleg')
    gebouwen = list()

    for line in lines:
        items = line.split(' ')
        try:
            uitleg = items[3]
        except IndexError:
            uitleg = ''
        gebouwen.append(Gebouw(int(items[0]), items[1], items[2], uitleg))

    return gebouwen


def parse1():
    with open('lijst.txt') as f:
        lines = list(f)

    lines = lines[2:]
    Gebouw = namedtuple('Gebouw', 'nummer afkorting naam')
    gebouwen = list()

    for line in lines:
        items = line.split('\t')
        gebouwen.append(Gebouw(int(items[0]), items[1].strip(), items[2].strip()))

    return gebouwen
