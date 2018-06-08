'''
Laat de gebouwen (en kunstwerken) op campus zien die je wilt zien. Er zijn een aantal argumenten die je kan meegeven, met -h zie je die.
Ze kunnen ook samen gebruikt worden. Een paar voorbeelden daarvan:
    `python3 gebouwen.py -ka 7 -m '1e 2e'`  # laat kunstwerken & gebouwen zien, lengte 7, waar letters van index 1 en 2 'e' zijn
    `python3 gebouwen.py -b vl -e er`       # laat gebouwen zien die beginnen met 'vl' en eindigen met 'er'
    `python3 gebouwen.py -ka 7 -l er`       # laat kunstwerken & gebouwen zien, lengte 7, met letters 'er' ergens in de naam.


Van een aantal kunstwerken zijn de varianten met en zonder spatie erin gezet, zoals HetDing.
Op een puzzel zou namelijk best wel 'hetding' kunnen komen, maar ook 'het ding'.

Alle straatnamen staan er ook in, als kunstwerken.

Alles is hoofdletterongevoelig, dus `-b wa` pakt Waaier.

'''
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
    gebouwen = [Gebouw(int(x[0][0]), x[0][1], x[0][2]) for x in
                zip([[item for item in line.split('\t')]
                    for line in open('buildings.txt').read().split('\n')[1:-1]])]

    kunstwerken = [Kunst(x[0][0]) for x in
                   zip([[item for item in line.split('\t')]
                       for line in open('kunst.txt').read().split('\n')[1:-1]])]

    return gebouwen, kunstwerken


if __name__ == '__main__':
    gebouwen, kunstwerken = parse_new()
    total = gebouwen + kunstwerken
    check = total if args.kunst else gebouwen

    if args.begin:
        check = [x for x in check if x.name.lower()[:len(args.begin)] == args.begin.lower()]
    if args.midden:
        indices = {int(x[0]): x[1] for x in args.midden.split(' ')}
        check = [x for x in check if all(x.name.lower()[min(len(x) - 1, p)] == indices[p] for p in indices.keys())]
    if args.eind:
        check = [x for x in check if x.name.lower()[-len(args.eind):] == args.eind.lower()]
    if args.letters:
        check = [x for x in check if all([l in x.name.lower() for l in args.letters.lower()])]
    if args.aantal:
        check = [x for x in check if len(x.name) == args.aantal]
    print(check)
