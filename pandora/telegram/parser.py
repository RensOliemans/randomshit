import re
# import datetime

import bs4
import parsedatetime as pdt

from collections import namedtuple

cal = pdt.Calendar()

FILENAME = 'berichten.html'
MINIMAL_DIFFERENCE = 3 * 60  # 3 minutes
MEETING_TIME = cal.parseDT('20:00')[0]

Puzzle = namedtuple('Puzzle', 'number team date')


def main():
    html = open(FILENAME).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = [x for x in soup.children if x not in ['\n', '', ' ']]
    day_breaks = analyse_days(items)
    day_breaks.insert(0, 0)
    day_breaks.append(-1)
    days = list()
    for i, x in enumerate(day_breaks):
        if i == len(day_breaks) - 1:
            break
        y = day_breaks[i+1]
        days.append(items[x:y])
    print('Possible puzzles next to bonuspuzzles (a bonuspuzzle was found '
          'within {} seconds of these puzzles).'.format(MINIMAL_DIFFERENCE))
    for day, elements in enumerate(days):
        print('Day %s' % day)
        puzzles = parse_items(elements)
        possible_puzzles = analyse(list(puzzles))
        print(*list(possible_puzzles), sep='\n')


def tester():
    html = open(FILENAME).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = [x for x in soup.children if x not in ['\n', '', ' ']]
    return items


def analyse_days(items):
    days = list()
    previous = None
    for item in items:
        date = item.find(attrs={'class': 'im_message_date_text'})
        if date:
            date = date.attrs['data-content']
            day = cal.parseDT(date)[0]
            if (previous is not None and previous.hour < MEETING_TIME.hour
               and day.hour == MEETING_TIME.hour):
                days.append(items.index(item))
            previous = day
    return days


def analyse(puzzles):
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
        elif contents:
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

    puzzle = Puzzle(number, team, cal.parseDT(date)[0])
    return puzzle


if __name__ == '__main__':
    main()
