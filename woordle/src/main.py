import os
import datetime
import re
import logging
from dataclasses import dataclass

from parsers import GameParser, is_new_message_line
from errors import NoScoreError

LOG_FILE = "out.log"
INPUT_FILE = os.path.join("..", "data", "chat.txt")


class Message:
    date: datetime.date
    person: str
    game: str
    number: int
    score: float


num_re = r"[0-9]+"
basic_score_re = r"[1-6X]/6"

parsers = [
    GameParser("Wordle", rf"Wordle (?P<num>{num_re}) (?P<score>{basic_score_re}\*?)\n"),
    GameParser("Woordle", rf"Woordle (?P<num>{num_re}) (?P<score>{basic_score_re})\n"),
    GameParser(
        "Woordle6", rf"Woordle6 (?P<num>{num_re}) (?P<score>{basic_score_re})\n"
    ),
    GameParser(
        "Worldle",
        r"#Worldle (?P<num>#[0-9]+) (?P<score>[1-6X]/6 (?:\([0-9]{1,3}%\))?(?: 🙈)?)\n",
    ),
    GameParser(
        "Squardle",
        r"I won Daily Squardle (?P<num>#[0-9]+) with (?P<score>[0-9]+) guess(?:es)? to spare!\n",
    ),
    GameParser(
        "Squardle",
        r"I solved (?P<score>[0-9]{1,2}/21) squares in Daily Squardle (?P<num>#[0-9]+)\n",
    ),
    GameParser(
        "Crosswordle", r"Daily Crosswordle (?P<num>[0-9]+): (?P<score>[\w ]+) .*\n"
    ),
    GameParser("Primel", rf"Primel (?P<num>{num_re}) (?P<score>{basic_score_re})"),
    GameParser("Letterle", r"Letterle(?P<num> )(?P<score>[0-9]{1,2}/26)"),
    GameParser(
        "Not Wordle", rf"Not Wordle (?P<num>{num_re}) (?P<score>{basic_score_re})\n"
    ),
    GameParser(
        "Nerdle",
        rf"(?:Nerdle|nerdlegame) (?P<num>{num_re}) (?P<score>{basic_score_re})\n",
    ),
    GameParser("Vardle", rf"Vardle (?P<num>{num_re}) (?P<score>[1-8X]/8)\n"),
]


def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    messages = list(parse_messages(lines))
    games = {m.game for m in messages}

    for game in games:
        show_average(game, [m for m in messages if m.game == game])


def show_average(game, messages):
    print(f"Showing stats for {game}")
    persons = {m.person for m in messages}
    max_person = max([len(p) for p in persons])
    for person in sorted(list(persons)):
        p_msgs = [m for m in messages if m.person == person]
        try:
            scores = [re.match(r"([0-9X]+)/[0-9]+", m.score).groups(1) for m in p_msgs]
        except AttributeError:
            fallbacks[game](person, p_msgs, max_person)
            continue
        fails = [s[0] for s in scores if s[0] == "X"]
        success = [int(s[0]) for s in scores if s[0] != "X"]
        print(
            f"{person.ljust(max_person)}: {len(p_msgs)} games, {len(fails)} failed attempts. "
            + f"Average score: {sum(success) / len(success):.2f} "
            + "for the completed games."
        )

    print("=====================\n")


def show_crosswordle(person, messages, ljust):
    scores = [
        re.match(r"([0-9]+)?(?:m )?([0-9]+)s", m.score).groups() for m in messages
    ]
    seconds = sum(
        [int(x[-1]) + 60 * int(x[0]) if len(x) > 1 else int(x[-1]) for x in scores]
    )
    print(
        f"{person.ljust(ljust)}: {len(messages)} games, average time of "
        + f"{seconds / len(messages):.0f}s"
    )


def show_squardle(person, messages, ljust):
    fails = [m for m in messages if "/" in m.score]
    success = [int(m.score) for m in messages if m not in fails]
    print(
        f"{person.ljust(ljust)}: {len(messages)} games, {len(fails)} failed attempts. "
        + f"Average guesses left: {sum(success) / len(success):.1f} "
        + "for the completed games."
    )


fallbacks = {
    "Crosswordle": show_crosswordle,
    "Squardle": show_squardle,
}


def parse_messages(lines):
    messages = list(group(iter(lines)))

    for message in messages:
        message = "\n".join(message)
        try:
            yield parse_message(message)
        except NoScoreError:
            logging.info("Message %s was not a scoring message, skipping.", message)
            continue


def group(lines):
    while lines:
        line = next(lines)
        message = [line]
        try:
            line = next(lines)
            while not is_new_message_line(line):
                message.append(line)
                line = next(lines)
        except StopIteration:
            yield message
            break
        yield message


def parse_message(message):
    """
    Method that takes a message from a chat and returns a Message object.
    Throws NoScoreError if the message doesn't contain a score.
    """
    for parser in parsers:
        if parser.can_parse(message):
            return parser.parse(message)

    logging.info("Couldn't parse %s", message)
    raise NoScoreError()


if __name__ == "__main__":
    logging.basicConfig(
        filename=LOG_FILE, filemode="w", encoding="utf-8", level=logging.DEBUG
    )
    main(INPUT_FILE)
