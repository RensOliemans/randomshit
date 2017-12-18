import datetime

FILENAME = 'chat.txt'
EMOTICON_UNI = '\U0001f4a9'
# todo: change
NAME_RENS = '***'
NAME_IRIS = '***'


def parse_file(filename):
    f = open(filename)
    iris, rens = list(), list()
    for line in f:
        day = parse_line(line)
        if day is None:
            continue
        if day.person == NAME_RENS:
            rens.append(day)
        elif day.person == NAME_IRIS:
            iris.append(day)
    return iris, rens


def count(filename):
    iris, rens = parse_file(filename)
    print("Iris: {} times. Rens: {} times".format(len(iris), len(rens)))


def average_times(filename):
    iris, rens = parse_file(filename)
    total = iris + rens

    def average_time(person):
        times = list()
        for poop in person:
            seconds = poop.date.hour * 60 * 60 + poop.date.minute * 60 + poop.date.second
            times.append(seconds)
        avg_seconds = sum(times) / len(times)
        m, s = divmod(avg_seconds, 60)
        h, m = divmod(m, 60)
        return h, m, s

    iris_time = average_time(iris)
    rens_time = average_time(rens)
    total_time = average_time(total)

    return iris_time, rens_time, total_time


def parse_line(line):
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


class Day(object):
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
