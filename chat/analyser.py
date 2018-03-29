""" Analyses Whatsapp chats hehe. """
import datetime

FILENAME = 'chat.txt'
# Poop icon
EMOTICON_UNI = '\U0001f4a9'
# Change this if the names change
NAME_RENS = 'Rens Oliemans'
NAME_IRIS = 'Iris <3'
NIGHT_HOUR = 4


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
        # mm/dd/yy, hh:mm - PERSON: CHAT_TEXT

        # metadata[0] = mm/dd/yy, hh:mm, metadata[1] = PERSON: CHAT_TEXT
        metadata = line.split(' - ')
        # person[0] = PERSON, person[1] = CHAT_TEXT
        person = metadata[1].split(':')[0]
        # metadata[0] = hh/dd/yy, metdata[1] = hh:mm
        metadata = metadata[0].split(', ')
        # date[0] = mm, date[1] = dd, date[2] = yy
        date = metadata[0].split('/')
        # time[0] = hh, time[1] = mm
        time = metadata[1].split(':')

        # stupid american date format (mm/dd/yy)
        day = int(date[1])
        month = int(date[0])
        year = int(date[2]) + 2000  # yy instead of yyyy, so add 2000

        hour = int(time[0])
        minute = int(time[1])
        date = datetime.datetime(year, month, day, hour, minute)
    if date and person:
        return Day(date, person)
    return None


def average_times(iris, rens):
    """
    Determines the average times of the day two people took a shit.
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
            if poop_hour <= NIGHT_HOUR:
                # in the night, add 24 hours so it's counted as night
                poop_hour = poop_hour + 24
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
        first_poop = person[0].date
        last_poop = person[-1].date
        difference = last_poop - first_poop

        # datetime.timedelta has days and seconds (the difference between two
        # dates), convert to days
        seconds_in_day = 24 * 60 * 60
        seconds = difference.days * seconds_in_day + difference.seconds
        days = seconds / seconds_in_day

        return days / len(person)

    iris_frequency = frequency(iris)
    rens_frequency = frequency(rens)
    return iris_frequency, rens_frequency


def main():
    """ Main method. """
    iris, rens = parse_file(FILENAME)
    print("Counter:\nIris: {}, Rens: {}, Total: {}\n"
          .format(len(iris), len(rens), len(iris + rens)))

    iris_time, rens_time, total_time = average_times(iris, rens)
    print("Average poop time (before {} will be counted as night, so "
          "+ 24 hours):\nIris: {}, Rens: {}, Total: {}"
          .format(NIGHT_HOUR, iris_time, rens_time, total_time))

    iris_frequency, rens_frequency = frequencies(iris, rens)
    print("Average frequency:\n"
          "Iris: one poop per {:.2f} days, Rens: one poop per {:.2f} days"
          .format(iris_frequency, rens_frequency))
    print("Average frequency:\n"
          "Iris: {:.2f} poops per day, Rens: {:.2f} poops per day"
          .format(1 / iris_frequency, 1 / rens_frequency))


class Day(object):
    """ Represents a single day, belonging to a person. """
    def __init__(self, date, person):
        self.date = date
        self.person = person

    def __str__(self):
        return "{} on {} at {}".format(
            self.person,
            str(self.date.time()),
            str(self.date.date()))

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    main()
