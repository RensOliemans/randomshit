import re
from collections import namedtuple
from datetime import datetime

import bs4


Puzzle = namedtuple('Puzzle', 'number team date')

FILENAME = 'berichten.html'
MINIMAL_DIFFERENCE = 3 * 60  # 3 minutes

# is used to determine when a day ended and when the next day starts
MEETING_TIME = datetime.strptime('20:00', '%H:%M')
TIME_FORMAT = '%I:%M:%S %p'


def main():
    html = open(FILENAME).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = [x for x in soup.children if x not in ['\n', '', ' ']]
    day_breaks = list(analyse_days(items))
    days = convert_to_days(items, day_breaks)

    print(f'Possible puzzles next to bonuspuzzles (a bonuspuzzle was found '
          f'within {MINIMAL_DIFFERENCE} seconds of these puzzles).')
    for day, elements in enumerate(days):
        print('Day %s' % day)
        puzzles = list(parse_items(elements))
        possible_puzzles = list(analyse(puzzles))
        print(*possible_puzzles, sep='\n')


def convert_to_days(items, indices):
    ''' slices all items into seperate days. the points where the new days begin
    are given by indices. '''
    # for slicing
    indices.insert(0, 0)
    indices.append(-1)
    for i, x in enumerate(indices):
        if i == len(indices) - 1:
            break
        y = indices[i+1]
        yield items[x:y]


def tester():
    ''' used for testing '''
    html = open(FILENAME).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = [x for x in soup.children if x not in ['\n', '', ' ']]
    return items


def analyse_days(items):
    ''' takes a list of (all) items, determines at what indices the new days
    begin. '''
    previous = None
    for item in items:
        date = item.find(attrs={'class': 'im_message_date_text'})
        if date:
            date = date.attrs['data-content']
            day = datetime.strptime(date, '%I:%M:%S %p')
            # day = cal.parseDT(date)[0]
            if (previous is not None and previous.hour < MEETING_TIME.hour
               and day.hour >= MEETING_TIME.hour):
                # new day; first message after meeting time
                yield items.index(item)
            previous = day


def analyse(puzzles):
    ''' takes a list of puzzles and determines what puzzles are close enough
    to a bonuspuzzle. '''
    for puzzle in puzzles:
        if puzzle.number != 'bonus':
            continue

        for other_puzzle in puzzles:
            if (puzzle == other_puzzle
               or puzzle.team != other_puzzle.team
               or other_puzzle.number == 'bonus'):
                continue
            if abs(puzzle.date - other_puzzle.date).seconds < MINIMAL_DIFFERENCE:
                yield other_puzzle


def parse_items(items):
    ''' gets a list of items and converts them to puzzles. '''
    for item in items:
        message = item.find(attrs={'class': 'im_message_text'})
        if message is None:
            # most likely some weird message
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
        elif contents:
            text = contents[0]
            date = item.find(attrs={'class': 'im_message_date_text'}).attrs['data-content']
            puzzle = parse_item(text, date)
            if puzzle:
                yield puzzle


def parse_item(text, date):
    '''
    takes the contents of a telegram messages and its timestamp, and returns
    a puzzle namedtuple. returns None if it wasn't corret (f.e. kill message).
    '''
    try:
        # TODO: change regex, depending on what team names are allowed.
        # In Pandora 2018, the following characters were used in the team names:
        # letters, numbers, spaces, apostrophe, dash, forward slash, asterisk,
        # period.
        # Formats:
        # <team> solved puzzle x[ and got a time bonus of y]?
        # <team> solved a bonuspuzzle
        m = re.match(r"(?P<team>(\w|\ |\'|\-|\/|\*|\.)+) solved ((?P<bonus>a bonuspuzzle)|puzzle (?P<number>\d))", text)
        if m is None:
            # In the first 2 Pandora days, the message format was different.
            # Formats:
            # [Puzzle solved] <team> solved puzzle number x[ and got a time bonus of y]?
            # [Puzzle solved] <team> solved a bonuspuzzle
            m = re.match(r"\[Puzzle solved\] (?P<team>(\w|\ |\'|\-|\/|\*|\.)+) solved ((?P<bonus>a bonuspuzzle)|puzzle (?P<number>\d))", text)
    except TypeError as e:
        # incorrect type - not a 'regular' message by the bot
        return
    if m is None:
        # no match found, likely a kill instead of a puzzle
        return
    team = m.group('team')
    number = 'bonus' if m.group('bonus') else int(m.group('number'))

    puzzle = Puzzle(number, team, datetime.strptime(date, '%I:%M:%S %p'))
    return puzzle


if __name__ == '__main__':
    main()
