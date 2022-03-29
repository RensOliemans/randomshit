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

    messages = list(parse_messages(lines))
    games = {m.game for m in messages}

    for game in games:
        show_average(game, [m for m in messages if m.game == game])


def show_average(game, messages):
    print(f"Showing stats for {game}")
    persons = {m.person for m in messages}
    for person in persons:
        p_msgs = [m for m in messages if m.person == person]
        try:
            scores = [re.match(r"([0-9X]+)/[0-9]+", m.score).groups(1) for m in p_msgs]
        except AttributeError:
            fallbacks[game](person, p_msgs)
            continue
        fails = [s[0] for s in scores if s[0] == "X"]
        success = [int(s[0]) for s in scores if s[0] != "X"]
        print(
            f"{person} has played {len(p_msgs)} times, has failed {len(fails)} times, "
            + f"and has an average score of {sum(success) / len(success):.2f} "
            + "for the games that they did succeed."
        )

    print("=====================\n")


def show_crosswordle(person, messages):
    scores = [
        re.match(r"([0-9]+)?(?:m )?([0-9]+)s", m.score).groups() for m in messages
    ]
    seconds = sum(
        [int(x[-1]) + 60 * int(x[0]) if len(x) > 1 else int(x[-1]) for x in scores]
    )
    print(
        f"{person} has played {len(messages)} times, and has taken on average "
        + f"{seconds / len(messages):.0f}s"
    )


def show_squardle(person, messages):
    scores = [int(m.score) for m in messages]
    # print(scores)


fallbacks = {
    "Crosswordle": show_crosswordle,
    "Squardle": show_squardle,
}


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
    return Message(date, person, game, number, score)


def parse_begin(line):
    begin_re = r"([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{2}:[0-9]{2}) - ([\s\S]+)"
    m = re.match(begin_re, line)
    if not m:
        raise NoScoreError()

    return m.groups()


def parse_person(line):
    person_re = r"([\w <]+): ([\s\S]+)"

    m = re.match(person_re, line)
    if not m:
        raise NoScoreError()

    return m.groups()


def parse_game(line):
    num_re = r"[0-9]+"
    basic_score_re = r"[1-6X]/6"
    wordle_re = rf"(Wordle) ({num_re}) ({basic_score_re}\*?)\n"
    woordle_re = rf"(Woordle) ({num_re}) ({basic_score_re})\n"
    woordle6_re = rf"(Woordle6) ({num_re}) ({basic_score_re})\n"
    worldle_re = r"(#Worldle) (#[0-9]+) ([1-6X]/6 (?:\([0-9]{1,3}%\))?(?: 🙈)?)\n"
    squardle_re = (
        r"I won Daily (Squardle) (#[0-9]+) with ([0-9]+) guess(?:es)? to spare!\n"
    )
    cross_re = r"Daily (Crosswordle) ([0-9]+): ([\w ]+) .*\n"
    primel_re = rf"(Primel) ({num_re}) ({basic_score_re})"
    letterle_re = r"(Letterle)( )([0-9]{1,2}/26)"
    not_wordle_re = rf"(Not Wordle) ({num_re}) ({basic_score_re})\n"
    nerdle_re = rf"(Nerdle|nerdlegame) ({num_re}) ({basic_score_re})\n"
    vardle_re = rf"(Vardle) ({num_re}) ([1-8X]/8)\n"

    for r in [
        wordle_re,
        woordle_re,
        woordle6_re,
        worldle_re,
        squardle_re,
        cross_re,
        primel_re,
        letterle_re,
        not_wordle_re,
        nerdle_re,
        vardle_re,
    ]:
        m = re.match(r, line)
        if not m:
            continue
        return m.groups()

    logging.info("Couldn't parse %s", line)
    raise NoScoreError()


if __name__ == "__main__":
    logging.basicConfig(
        filename="out.log", filemode="w", encoding="utf-8", level=logging.DEBUG
    )
    main()
