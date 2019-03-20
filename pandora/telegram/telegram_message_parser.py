import itertools
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

TEAM_PATTERN = r"(?P<team>(\w|\ |\'|\-|\/|\*|\.)+)"
BONUS_PATTERN = r"(?P<bonus>a bonuspuzzle)"
PUZZLE_PATTERN = r"puzzle (?P<number>\d)"
SOLVED_PATTERN = r"\[Puzzle solved\] "


class MessageIsOfIncorrectFormat(Exception):
    pass


def main():
    html_parser = build_html_parser(FILENAME)
    all_messages = get_messages_from_html(html_parser)
    indices_of_first_messages_of_days = determine_indices_of_first_messages_per_day(all_messages)
    messages_per_day = split_messages_into_days(all_messages, indices_of_first_messages_of_days)

    print(f'Possible puzzles next to bonuspuzzles (a bonuspuzzle was found '
          f'within {MINIMAL_DIFFERENCE} seconds of these puzzles).')
    for day, messages_of_day in enumerate(messages_per_day):
        print(f"Day {day}")
        all_puzzles_of_day = convert_messages_to_puzzles(messages_of_day)
        puzzles_close_to_bonuspuzzles = get_close_enough_puzzles(all_puzzles_of_day)
        pretty_print(puzzles_close_to_bonuspuzzles)


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
    start_index = 0
    messages_per_day = list()

    for _, end_index in enumerate(indices_of_first_messages_of_days):
        messages_per_day.append(all_messages[start_index:end_index])
        start_index = end_index
    messages_per_day.append(all_messages[start_index:])  # Don't forget the last day
    return messages_per_day


def convert_messages_to_puzzles(messages_per_day):
    puzzles_of_day = list()
    for message in messages_per_day:
        try:
            message_contents, message_date = get_message_contents(message)
        except MessageIsOfIncorrectFormat:
            continue

        if len(message_contents) > 0:
            message_contents = remove_tags_from_message_contents(message_contents)
        puzzles_of_day.extend(convert_message_contents_to_puzzles(message_contents, message_date))
    return puzzles_of_day


def get_message_contents(message):
    message_text_div = message.find(attrs={'class': 'im_message_text'})
    message_date = message.find(attrs={'class': 'im_message_date_text'})

    if message_text_div is None or message_date is None:
        raise MessageIsOfIncorrectFormat("Message is of the wrong format.")

    return message_text_div.contents, message_date.attrs['data-content']


def remove_tags_from_message_contents(message_contents):
    return [x for x in message_contents if type(x) != bs4.element.Tag]


def convert_message_contents_to_puzzles(message_contents, message_date):
    for text in message_contents:
        try:
            puzzle = get_puzzle(text, message_date)
            yield puzzle
        except MessageIsOfIncorrectFormat:
            continue


def get_puzzle(message_text, message_date):
    result = get_team_and_puzzle_number_from_message(message_text)
    number, team = result
    return Puzzle(number, team, datetime.strptime(message_date, TIME_FORMAT))


def get_team_and_puzzle_number_from_message(message_text):
    match = get_message_regex_match(message_text)
    if match is None:
        raise MessageIsOfIncorrectFormat("Could not parse the message regex, was likely a kill "
                                         "message of some sorts instead of a puzzle message.")
    team = match.group('team')
    number = 'bonus' if match.group('bonus') else int(match.group('number'))
    return number, team


def get_message_regex_match(message_text):
    try:
        message_pattern = f"{TEAM_PATTERN} solved ({BONUS_PATTERN}|{PUZZLE_PATTERN})"
        match = re.match(message_pattern, message_text)
        if match is None:
            match = re.match(SOLVED_PATTERN + message_pattern, message_text)
    except TypeError:
        raise MessageIsOfIncorrectFormat("Message was of wrong type, was not a regular message"
                                         "and likely a leaderboard/status message")
    return match


def get_close_enough_puzzles(puzzles):
    for (puzzle, other_puzzle) in itertools.combinations(puzzles, 2):
        if not only_one_of_puzzles_is_bonus(puzzle, other_puzzle):
            continue
        if puzzle.team != other_puzzle.team:
            continue
        if two_puzzles_are_close_enough(puzzle, other_puzzle):
            yield puzzle_that_is_not_bonus(puzzle, other_puzzle)


def only_one_of_puzzles_is_bonus(puzzle, other_puzzle):
    return (puzzle.number == 'bonus') != (other_puzzle.number == 'bonus')


def two_puzzles_are_close_enough(puzzle, other_puzzle):
    return abs(puzzle.date - other_puzzle.date).seconds < MINIMAL_DIFFERENCE


def puzzle_that_is_not_bonus(puzzle, other_puzzle):
    return puzzle if puzzle.number == 'bonus' else other_puzzle


def pretty_print(puzzles):
    for puzzle in puzzles:
        date = puzzle.date
        print(f"Number {puzzle.number}.\tTeam "
              f"{puzzle.team[:12]:.<12}\tTime: {date.hour}:{date.minute}:{date.second}")


if __name__ == '__main__':
    main()
