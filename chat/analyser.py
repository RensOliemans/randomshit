""" Analyses Whatsapp chats hehe. """
import datetime
import re
import matplotlib.pyplot as plt
import sqlite3
from converter import Message

FILENAME = "chats/db.sqlite"
# Time at which the poop becomes counted as next day
NIGHT_HOUR = 4


# Relevant for format of the messages
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MESSAGE_PATTERN = r"(?P<date>(\S|\s)+)--(?P<person>(\w|\s)+)--(?P<message>(\S|\s)+)"
message_prog = re.compile(MESSAGE_PATTERN)

# Poop icon
EMOTICON_UNI = "\U0001f4a9"
NAME_RENS = "Rens"
NAME_IRIS = "Iris"


def parse_file(filename):
    """
    Parses an entire file.

    :param filename: name of the file
    :returns two lists of days, belonging to two people
    """
    chat = get_messages(filename)
    rens = [
        message
        for message in chat
        if message is not None and message.person == NAME_RENS
    ]
    iris = [
        message
        for message in chat
        if message is not None and message.person == NAME_IRIS
    ]
    return iris, rens


def get_messages(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    messages = c.execute("SELECT * FROM messages").fetchall()
    conn.close()
    return [
        Message(datetime.datetime.strptime(m[0], DATE_FORMAT), m[1], m[2])
        for m in messages
    ]


def average_times(iris, rens):
    """
    Determines the average times of the day two people took a shit.
    :param iris: list of Day objects belonging to Iris
    :param rens: list of Day objects belonging to Rens
    """
    total = iris + rens

    def average_time(person):
        """Determines the average shit time of a single person."""
        if not person:
            raise ValueError(
                "Pooped zero times, can't calculate average time "
                "(are the names correct?)"
            )
        times = list()
        for poop in person:
            poop_hour = poop.date.hour
            # add 24 hours if it's between 00:00 and NIGHT_HOUR it's counted as night
            poop_hour = poop_hour + 24 if poop_hour <= NIGHT_HOUR else poop_hour
            poop_minutes = poop_hour * 60 + poop.date.minute
            times.append(poop_minutes)
        avg_minutes = sum(times) / len(times)
        hour, minute = divmod(avg_minutes, 60)
        return datetime.time(hour=int(hour), minute=int(minute))

    iris_time = average_time(iris)
    rens_time = average_time(rens)
    total_time = average_time(total)

    return iris_time, rens_time, total_time


def frequencies(iris, rens):
    """Determines the frequencies of two people."""

    def frequency(person):
        """Determines the frequencies of one person."""
        if not person:
            raise ValueError(
                "Pooped zero times, can't calculate average time "
                "(are the names correct?)"
            )
        first_poop, last_poop = min(person).date, max(person).date
        difference = last_poop - first_poop

        # datetime.timedelta has days and seconds (the difference between two
        # dates), convert to days
        seconds_in_day = 24 * 60 * 60
        seconds = difference.days * seconds_in_day + difference.seconds
        days = seconds / seconds_in_day

        return days, days / len(person)

    iris_days, iris_frequency = frequency(iris)
    rens_days, rens_frequency = frequency(rens)
    average_days = (iris_days + rens_days) / 2
    return average_days, iris_frequency, rens_frequency


def get_date_list(iris, rens):
    first_date: Day = min(min(iris), min(rens))
    last_date: Day = max(max(iris), max(rens))
    total_days = (last_date.date - first_date.date).days

    return [
        first_date.date.date() + datetime.timedelta(days=x) for x in range(total_days)
    ]


def create_plot(iris, rens):
    sorted_iris = sorted(iris)
    sorted_rens = sorted(rens)

    date_list = get_date_list(sorted_iris, sorted_rens)
    iris_days = [i.date.date() for i in sorted_iris]
    rens_days = [r.date.date() for r in sorted_rens]
    iris_poops = {d: iris_days.count(d) for d in date_list}
    rens_poops = {d: rens_days.count(d) for d in date_list}

    x = date_list
    iris_y = build_y(iris_poops.values())
    rens_y = build_y(rens_poops.values())
    build_plt(x, iris_y, rens_y)


def build_plt(x, iris_y, rens_y):
    fig, ax = plt.subplots()
    ax.plot(x, iris_y, color="tab:blue", label="Iris")
    ax.plot(x, rens_y, color="tab:orange", label="Rens")
    plt.legend(loc="lower right")
    fig.savefig("test.pdf", format="pdf")


def build_y(poops):
    total = 0
    result = [0 for _, _ in enumerate(poops)]
    for i, elem in enumerate(poops):
        result[i] = total + elem
        total += elem
    return result


def main():
    """Main method."""
    iris, rens = parse_file(FILENAME)
    days, iris_frequency, rens_frequency = frequencies(iris, rens)
    print(
        "Counter:\nIris: {}, Rens: {}, Total: {}, over {:.2f} days.\n".format(
            len(iris), len(rens), len(iris + rens), days
        )
    )

    iris_time, rens_time, total_time = average_times(iris, rens)
    print(
        "Average poop time (before {} will be counted as night, so "
        "+ 24 hours):\nIris: {}, Rens: {}, Total: {}".format(
            NIGHT_HOUR, iris_time, rens_time, total_time
        )
    )

    # regular frequency
    print(
        "Average frequency:\n"
        "Iris: one poop per {:.2f} days, Rens: one poop per {:.2f} days".format(
            iris_frequency, rens_frequency
        )
    )
    # inverse frequency
    print(
        "Average frequency:\n"
        "Iris: {:.2f} poops per day, Rens: {:.2f} poops per day".format(
            1 / iris_frequency, 1 / rens_frequency
        )
    )
    create_plot(iris, rens)


class Day(object):
    """Represents a single day, belonging to a person."""

    def __init__(self, date, person):
        self.date = date
        self.person = person

    def __str__(self):
        return f"{self.person} on {str(self.date.moment())}, at {str(self.date.date())}"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date


if __name__ == "__main__":
    main()
