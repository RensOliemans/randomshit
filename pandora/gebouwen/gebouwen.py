"""
Laat de gebouwen (en kunstwerken) op campus zien die je wilt zien.
Er zijn een aantal argumenten die je kan meegeven, met -h zie je die.
Ze kunnen ook samen gebruikt worden. Een paar voorbeelden daarvan:
    # laat kunstwerken & gebouwen zien, lengte 7, waar letters van index 1 en 2 'e' zijn
    `python3 gebouwen.py -ka 7 -m '1e 2e'`

    # laat gebouwen zien die beginnen met 'vl' en eindigen met 'er'
    `python3 gebouwen.py -b vl -e er`

    # laat kunstwerken & gebouwen zien, lengte 7, met letters 'er' ergens in de naam.
    `python3 gebouwen.py -ka 7 -l er`


Van een aantal kunstwerken zijn de varianten met en zonder spatie erin gezet, zoals HetDing.
Op een puzzel zou namelijk best wel 'hetding' kunnen komen, maar ook 'het ding'.

Alle straatnamen staan er ook in, als kunstwerken.

Alles is hoofdletterongevoelig, dus `-b wa` pakt Waaier.

''"""
import argparse

from buildings import Building, Artwork

parser = argparse.ArgumentParser(description='Get all buildings (and artworks) on the UT.')
parser.add_argument('-l', '--letters', type=str,
                    help='what letters does the building have (somewhere in the name)')
parser.add_argument('-a', '--amount', type=int,
                    help='how many letters does the building have')
parser.add_argument('-b', '--begin', type=str,
                    help='what are the first letters of the building?')
parser.add_argument('-e', '--end', type=str,
                    help='what are the last letters of the building?')
parser.add_argument('-m', '--middle', type=str,
                    help='use: [<index><letter> ]+')
parser.add_argument('-w', '--work-of-art', dest='include_artworks', action='store_true',
                    help='take the works of art')


def main():
    buildings, artworks = get_buildings_and_artworks('buildings.txt', 'artworks.txt')

    filters = parser.parse_args()
    filtered_items = filter_items(buildings, artworks, filters)

    print(filtered_items)


def get_buildings_and_artworks(buildings_filename, artworks_filename):
    lines = get_lines_from_file(buildings_filename)
    buildings = list(parse_buildings_from_lines(lines))

    lines = get_lines_from_file(artworks_filename)
    artworks = list(parse_artworks_from_lines(lines))

    return buildings, artworks


def get_lines_from_file(filename):
    with open(filename) as f:
        lines = f.read().split('\n')[1:-1]
        return lines


def parse_buildings_from_lines(lines):
    for line in lines:
        columns = line.split('\t')
        number, name, abbreviation = columns[0], columns[1], columns[2]
        yield Building(int(number), name, abbreviation)


def parse_artworks_from_lines(lines):
    for line in lines:
        columns = line.split('\t')
        name = columns[0]
        yield Artwork(name)


def filter_items(buildings, artworks, filters):
    if filters.include_artworks:
        filtered_items = apply_filters(buildings + artworks, filters)
    else:
        filtered_items = apply_filters(buildings, filters)
    return filtered_items


def apply_filters(items_to_filter, filters):
    if filters.begin:
        items_to_filter = apply_begin_filter(items_to_filter, filters.begin)
    if filters.middle:
        items_to_filter = apply_middle_filter(items_to_filter, filters.middle)
    if filters.end:
        items_to_filter = apply_end_filter(items_to_filter, filters.end)
    if filters.letters:
        items_to_filter = apply_some_letters_filter(items_to_filter, filters.letters)
    if filters.amount:
        items_to_filter = apply_amount_filter(items_to_filter, filters.amount)
    return items_to_filter


def apply_begin_filter(items, first_letters):
    return [x for x in items if x.name.lower()[:len(first_letters)] == first_letters.lower()]


def apply_middle_filter(items, middle_letters):
    indices = {int(x[0]): x[1] for x in middle_letters.split(' ')}
    return [x for x in items
            if all(x.name.lower()[min(len(x) - 1, p)] == indices[p]
                   for p in indices.keys())]


def apply_end_filter(items, last_letters):
    return [x for x in items if x.name.lower()[-len(last_letters):] == last_letters.lower()]


def apply_some_letters_filter(items, some_letters):
    return [x for x in items if all([l in x.name.lower() for l in some_letters.lower()])]


def apply_amount_filter(items, amount_of_letters):
    return [x for x in items if len(x.name) == amount_of_letters]


if __name__ == '__main__':
    main()
