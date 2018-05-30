import re

import bs4
import parsedatetime as pdt

from collections import namedtuple

cal = pdt.Calendar()

FILENAME = 'test.html'
MINIMAL_DIFFERENCE = 10 * 60  # 5 minutes

Puzzle = namedtuple('Puzzle', 'number team date')


def main():
    html = open(FILENAME).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = [x for x in soup.children if x not in ['\n', '', ' ']]
    puzzles = parse_items(items)
    possible_puzzles = analyse(list(puzzles))
    print(list(possible_puzzles))


def analyse(puzzles):
    for puzzle in puzzles:
        if puzzle.number != 'bonus':
            continue

        for other_puzzle in puzzles:
            if puzzle == other_puzzle or puzzle.team != other_puzzle.team or other_puzzle.number == 'bonus':
                continue
            if abs(puzzle.date - other_puzzle.date).seconds < MINIMAL_DIFFERENCE:
                yield other_puzzle


def parse_items(items):
    for item in items:
        message = item.find(attrs={'class': 'im_message_text'})
        if message is None:
            continue
        contents = message.contents
        if len(contents) > 1:
            # multiple bot messages in one messages, separated by <br\> tags
            # remove <br\> tags
            contents = [x for x in contents if type(x) != bs4.element.Tag]
            date = item.find(attrs={'class': 'im_message_date_text'}).attrs['data-content']
            for text in contents:
                # parse each item
                puzzle = parse_item(text, date)
                if puzzle:
                    yield puzzle
        else:
            text = contents[0]
            date = item.find(attrs={'class': 'im_message_date_text'}).attrs['data-content']
            puzzle = parse_item(text, date)
            if puzzle:
                yield puzzle


def parse_item(text, date):
    try:
        # TODO: change regex, depending on what team names are allowed
        # In Pandora 2018, the following characters were used:
        # letters, numbers, spaces, apostrophe, dash, forward slash, asterisk,
        # period
        m = re.match(r"(?P<team>(\w|\ |\'|\-|\/|\*|\.)+) solved ((?P<bonus>a bonuspuzzle)|puzzle (?P<number>\d))", text)
    except TypeError as e:
        # incorrect type - not a 'regular' message by the bot
        return
    if m is None:
        # no match found, likely a kill instead of a puzzle
        return
    team = m.group('team')
    number = 'bonus' if m.group('bonus') else int(m.group('number'))

    puzzle = Puzzle(number, team, cal.parseDT(date)[0])
    return puzzle


if __name__ == '__main__':
    main()
