import re
from datetime import datetime

FILENAME_IN = 'chat.txt'
FILENAME_DATA = 'messages'
IRIS = 'Iris'
RENS = 'Rens'
ALTERNATIEF = {IRIS: ['Iris <3'], RENS: ['Rens Oliemans']}

iris, rens = list(), list()


def main():
    items = get_items(FILENAME_DATA)

    with open(FILENAME_IN) as f:
        messages = list(f)
        for line in messages:
            item = parse_message(line)
            if item is None:
                continue
            if item.person not in ALTERNATIEF.keys():
                for key in ALTERNATIEF:
                    if item.person in ALTERNATIEF[key]:
                        item.person = key
            items.add(item)
        print(*items, sep='\n')

        fo = open(FILENAME_DATA, 'w')
        for item in items:
            fo.write(str(item))
            fo.write('\n')
            pass

        fo.close()


def parse_message(message, date_format='%d-%m-%y, %H:%M'):
    pattern = r"(?P<date>(\S| )+) - (?P<person>\w+): (?P<message>(\S| )+)"
    message.replace('\n', '')

    match = re.match(pattern, message)
    if match:
        date = match.group('date')
        person = match.group('person')
        message = match.group('message')
        date_object = datetime.strptime(date, date_format)
        return Message(date_object, person, message)
    else:
        # print(message)
        pass


def get_items(filename):
    f = open(filename)
    items = list(f)

    messages = set()
    for item in items:
        # It's been converted to datetime since then, so the format is different
        message = parse_message(item, date_format='%Y-%m-%d %H:%M:%S')
        messages.add(message)
    f.close()
    return messages


class Message:

    def __init__(self, date_time, person, message):
        self.date_time = date_time
        self.person = person
        self.message = message

    def __hash__(self):
        return int(self.date_time.timestamp())

    def __eq__(self, other):
        return hash(self) == hash(other) and type(other) == type(self)

    def __str__(self):
        return f"{self.date_time} - {self.person}: {self.message}"

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    main()
