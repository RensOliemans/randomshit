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
    html_parser = build_html_parser(FILENAME)
    all_messages = get_messages_from_html(html_parser)
    indices_of_first_messages_of_days = determine_indices_of_first_messages_per_day(all_messages)
    messages_per_day = split_messages_into_days(all_messages, indices_of_first_messages_of_days)

    # Old ugly code
    # items = all_messages
    # day_breaks = list(analyse_days(items))
    # days = convert_to_days(items, day_breaks)

    print(f'Possible puzzles next to bonuspuzzles (a bonuspuzzle was found '
          f'within {MINIMAL_DIFFERENCE} seconds of these puzzles).')
    for day, messages_of_day in enumerate(messages_per_day):
        print('Day %s' % day)
        puzzles = convert_messages_to_puzzles(messages_per_day)
        puzzles = list(parse_items(messages_of_day))
        possible_puzzles = list(analyse(puzzles))
        pretty_print(possible_puzzles)


def build_html_parser(filename):
    html_file = open(filename).read()
    return bs4.BeautifulSoup(html_file, 'html.parser')


def get_messages_from_html(html_parser):
    return [x for x in html_parser.children if x not in ['\n', '', ' ']]


def determine_indices_of_first_messages_per_day(messages):
    previous_message_datetime = None
    for index, current_message in enumerate(messages):
        current_message_datetime = get_datetime_of_message(current_message)
        if current_message_datetime is None:
            continue

        if message_is_first_of_the_day(current_message_datetime, previous_message_datetime):
            yield index
        previous_message_datetime = current_message_datetime


def get_datetime_of_message(message):
    message_datetime_span = message.find(attrs={'class': 'im_message_date_text'})
    if message_datetime_span:
        message_datetime_content = message_datetime_span['data-content']
        message_datetime_day = datetime.strptime(message_datetime_content, TIME_FORMAT)
        return message_datetime_day


def message_is_first_of_the_day(current_message_datetime, previous_message_datetime):
    if previous_message_datetime is None:
        return False

    previous_message_was_before_meeting = previous_message_datetime.hour < MEETING_TIME.hour
    current_message_datetime_was_after_meeting = current_message_datetime.hour >= MEETING_TIME.hour
    return previous_message_was_before_meeting and current_message_datetime_was_after_meeting


def split_messages_into_days(all_messages, indices_of_first_messages_of_days):
    begin_index = 0
    messages_per_day = list()

    for _, end_index in enumerate(indices_of_first_messages_of_days):
        messages_per_day.append(all_messages[begin_index:end_index])
        begin_index = end_index
    messages_per_day.append(all_messages[begin_index:])  # Don't forget the last day
    return messages_per_day


def convert_messages_to_puzzles(messages_per_day):
    for message in messages_per_day:
        message_text_div = message.find(attrs={'class': 'im_message_text'})
        if message_text_div is None:
            continue

        convert_message_contents_to_puzzle(message_text_div.contents)


def convert_message_contents_to_puzzle(message_contents):
    return

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


def convert_to_days(items, indices):
    ''' slices all items into seperate days. the points where the new days begin
    are given by indices. '''
    # for slicing
    indices.insert(0, 0)
    indices.append(-1)
    for i, x in enumerate(indices):
        if i == len(indices) - 1:
            break
        y = indices[i + 1]
        yield items[x:y]


def analyse_days(items):
    ''' takes a list of (all) items, determines at what indices the new days
    begin. '''
    previous = None
    for item in items:
        date = item.find(attrs={'class': 'im_message_date_text'})
        if date:
            date = date.attrs['data-content']
            day = datetime.strptime(date, TIME_FORMAT)
            # A new day begins when the previous message was before the start
            # of the meeting, and the next message is after the start of the
            # meeting
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


def parse_item(text, date):
    '''
    takes the contents of a telegram messages and its timestamp, and returns
    a puzzle namedtuple. returns None if it wasn't corret (f.e. kill message).
    '''
    try:
        # TODO: change regex, depending on what kind of messages are being sent
        # by the bot.
        # In Pandora 2018, the following characters were used in the team names:
        # letters, numbers, spaces, apostrophe, dash, forward slash, asterisk,
        # period.
        # Formats:
        # <team> solved puzzle x[ and got a time bonus of y]?
        # <team> solved a bonuspuzzle
        team = "(?P<team>(\w|\ |\'|\-|\/|\*|\.)+)"
        bonus = "(?P<bonus>a bonuspuzzle)"
        puzzle = "puzzle (?P<number>\d)"
        regex = fr"{team} solved ({bonus}|{puzzle})"
        m = re.match(regex, text)
        if m is None:
            # In the first 2 Pandora days, the message format was different.
            # The string
            #   [Puzzle solved]
            # was prepended to the string
            # Formats:
            # [Puzzle solved] <team> solved puzzle x[ and got a time bonus of y]?
            # [Puzzle solved] <team> solved a bonuspuzzle
            solved = "\[Puzzle solved\] "
            m = re.match(solved + regex, text)
    except TypeError:
        # incorrect type - not a 'regular' message by the bot
        # Example: The leaderboards. These aren't a string object, but
        # something weird (like <pre><code> `leaderboard` </code></pre>) and
        # re doesn't parse it
        return
    if m is None:
        # no match found, this is either:
        #  kill message
        #  team eliminated
        #  status messages by bot
        return
    team = m.group('team')
    number = 'bonus' if m.group('bonus') else int(m.group('number'))

    puzzle = Puzzle(number, team, datetime.strptime(date, TIME_FORMAT))
    return puzzle


def pretty_print(puzzles):
    for puzzle in puzzles:
        date = puzzle.date
        print(f"Number {puzzle.number}.\tTeam "
              f"{puzzle.team[:12]:.<12}\tTime: {date.hour}:{date.minute}:{date.second}")


if __name__ == '__main__':
    main()
