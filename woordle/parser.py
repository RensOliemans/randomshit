import datetime
import re
import logging
from dataclasses import dataclass


class NoScoreError(Exception):
    pass


@dataclass
class Message:
    date: datetime.date
    person: str
    game: str
    number: int
    score: float


def main():
    with open("chat.txt") as f:
        lines = f.readlines()

    messages = parse_messages(lines)
    # print('\n'.join([str(x) for x in messages]))
    list(messages)


def parse_messages(lines):
    while lines:
        line = lines.pop(0)
        try:
            yield parse_message(line)
        except NoScoreError:
            logging.info("Message %s was not a scoring message, skipping.", line)
            continue


def parse_message(line):
    # Method that takes a line and returns a Message.
    # Throws NoScoreError if the line doesn't contain a score.
    if ":" not in line:
        raise NoScoreError()

    date, rest = parse_begin(line)
    person, rest = parse_person(rest)
    game, number, score = parse_game(rest)
    # print(f"{date=}")
    # print(f"{person=}")
    # print(f"{rest=}")
    return Message(date, person, game, number, score)


def parse_begin(line):
    begin_re = r"([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{2}:[0-9]{2}) - ([\s\S]+)"
    m = re.match(begin_re, line)
    if not m:
        raise NoScoreError()

    return m.groups()


def parse_person(line):
    person_re = r"([\w ]+): ([\s\S]+)"

    m = re.match(person_re, line)
    if not m:
        raise NoScoreError()

    return m.groups()


def parse_game(line):
    num_re = r"[0-9]+"
    basic_score_re = r"[1-6X]/6"
    wordle_re = fr"(Wordle) ({num_re}) ({basic_score_re}\*?)\n"
    woordle_re = fr"(Woordle) ({num_re}) ({basic_score_re})\n"
    woordle6_re = fr"(Woordle6) ({num_re}) ({basic_score_re})\n"
    worldle_re = fr"(#Worldle) (#[0-9]+) ([1-6]/6 \([0-9]{1,3}%\)( 🙈)?)\n"

    for r in [wordle_re, woordle_re, woordle6_re, worldle_re]:
        m = re.match(r, line)
        if not m:
            continue
        return m.groups()

    logging.warning("Couldn't parse %s", line)
    raise NoScoreError()


if __name__ == "__main__":
    main()
