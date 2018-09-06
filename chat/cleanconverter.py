import re
from datetime import datetime

FILENAME_IN = 'chats/newchat.txt'
FILENAME_DATA = 'chats/messages'
NAMES = {'Iris': ['Iris <3'], 'Rens': ['Rens Oliemans']}
FORMATS = ['%d-%m-%y, %H:%M', '%Y-%m-%d %H:%M:%S', '%m/%d/%y, %H:%M']


def main():
    messages = set()
    with open(FILENAME_DATA) as f:
        # First get the stored data
        for row in list(f):
            message = parse_message(row)
            messages.add(message)

    with open(FILENAME_IN) as f:
        # Then get the 'new input'
        for row in list(f):
            message = parse_message(row)
            if message is None:
                continue

            message = replace_names(message)
            messages.add(message)
        print(len(messages))

    with open(FILENAME_DATA, 'w') as f:
        # Finally, write the (total) results to the data file
        for message in messages:
            f.write(str(message) + '\n')


def replace_names(message):
    if message.person in NAMES.keys():
        return message
    else:
        for key in NAMES:
            if message.person in NAMES[key]:
                message.person = key
                return message


def parse_message(message):
    # The \< and 3 are for the person name
    pattern = r"(?P<date>(\S| )+) - (?P<person>(\w|\<|3| )+): (?P<message>(\S| )+)"
    match = re.match(pattern, message)
    if match:
        date = match.group('date')
        person = match.group('person')
        message = match.group('message')
        for form in FORMATS:
            try:
                date_object = datetime.strptime(date, form)
            except ValueError as e:
                continue
        return Message(date_object, person, message)


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
