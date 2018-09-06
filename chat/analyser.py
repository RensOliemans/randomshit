""" Analyses Whatsapp chats hehe. """
import datetime

import parsedatetime

FILENAME = 'chats/messages'
# Poop icon
EMOTICON_UNI = '\U0001f4a9'
# Change this if the names change
NAME_RENS = 'Rens'
NAME_IRIS = 'Iris'
# Time at which the poop becomes counted as next day
NIGHT_HOUR = 4

cal = parsedatetime.Calendar()


def parse_file(filename):
    """
    Parses an entire file.

    :param filename: name of the file
    :returns two lists of days, belonging to two people
    """
    chat = open(filename)
    iris, rens = list(), list()
    for line in chat:
        day = parse_line(line)
        if day is None:
            continue
        if day.person == NAME_RENS:
            rens.append(day)
        elif day.person == NAME_IRIS:
            iris.append(day)
    return iris, rens


def parse_line(line):
    """
    Parses a single line.

    :param line: a single line in a txt file
    :returns a Day object if it is a valid line, None otherwise
    """
    date = None
    person = None
    if EMOTICON_UNI in line:
        # format of line:
        # mm-dd-yy, hh:mm - PERSON: CHAT_TEXT

        metadata = line.split(' - ')
        # metadata[0] = mm/dd/yy, hh:mm       metadata[1] = PERSON: CHAT_TEXT
        person = metadata[1].split(':')[0]
        # person[0]   = PERSON                person[1]   = CHAT_TEXT

        # Example of input: 15-05-18, 16:16
        date_format = '%Y-%m-%d %H:%M:%S'
        date = datetime.datetime.strptime(metadata[0], date_format)
        return Day(date, person)


def average_times(iris, rens):
    """
    Determines the average times of the day two people took a shit.
    :param iris: list of Day objects belonging to Iris
    :param rens: list of Day objects belonging to Rens
    """
    total = iris + rens

    def average_time(person):
        """ Determines the average shit time of a single person. """
        if not person:
            raise ValueError("Pooped zero times, can't calculate average time "
                             "(are the names correct?)")
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
    """ Determines the frequencies of two people. """

    def frequency(person):
        """ Determines the frequencies of one person. """
        if not person:
            raise ValueError("Pooped zero times, can't calculate average time "
                             "(are the names correct?)")
        first, last = get_extremes(person)
        first_poop = first.date
        last_poop = last.date
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


def get_extremes(poops):
    first, last = poops[0], poops[0]
    for poop in poops:
        if poop.date > last.date:
            last = poop
        if poop.date < first.date:
            first = poop
    return first, last


def main():
    """ Main method. """
    iris, rens = parse_file(FILENAME)
    days, iris_frequency, rens_frequency = frequencies(iris, rens)
    print("Counter:\nIris: {}, Rens: {}, Total: {}, over {:.2f} days.\n"
          .format(len(iris), len(rens), len(iris + rens), days))

    iris_time, rens_time, total_time = average_times(iris, rens)
    print("Average poop time (before {} will be counted as night, so "
          "+ 24 hours):\nIris: {}, Rens: {}, Total: {}"
          .format(NIGHT_HOUR, iris_time, rens_time, total_time))

    # regular frequency
    print("Average frequency:\n"
          "Iris: one poop per {:.2f} days, Rens: one poop per {:.2f} days"
          .format(iris_frequency, rens_frequency))
    # inverse frequency
    print("Average frequency:\n"
          "Iris: {:.2f} poops per day, Rens: {:.2f} poops per day"
          .format(1 / iris_frequency, 1 / rens_frequency))


class Day(object):
    """ Represents a single day, belonging to a person. """
    def __init__(self, date, person):
        self.date = date
        self.person = person

    def __str__(self):
        return f"{self.person} on {str(self.date.time())}, at {str(self.date.date())}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    main()
