'''
This module converts messages from WhatsApp to an internal representation,
so that multiple WhatsApp chats (even from different persons) can be combined
into one single output.
'''

import re
from datetime import datetime

# Relevant for files
FILE_DIRECTORY = 'chats'
FILENAME_INPUT = FILE_DIRECTORY + '/' + 'chat1.txt'
FILENAME_DATA = FILE_DIRECTORY + '/' + 'messages'

# Relevant for message format
NAMES = {'Iris': ['Iris <3'], 'Rens': ['Rens Oliemans']}
FORMATS = ['%d-%m-%y, %H:%M', '%Y-%m-%d %H:%M:%S', '%m/%d/%y, %H:%M']
# The \< and 3 are for the person name
PATTERN = r"(?P<date>(\S| )+) - (?P<person>(\w|\<|3| )+): (?P<message>(\S| )+)"
message_prog = re.compile(PATTERN)


def main():
    messages = set()
    with open(FILENAME_DATA) as f:
        # First get the stored data
        for row in list(f):
            message = parse_message(row)
            messages.add(message)

    with open(FILENAME_INPUT) as f:
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
    result = message_prog.match(message)
    if result:
        date = result.group('date')
        person = result.group('person')
        message = result.group('message')
        for form in FORMATS:
            try:
                date_object = datetime.strptime(date, form)
            except ValueError as e:
                # Try a different date format, another one might be the correct one
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
