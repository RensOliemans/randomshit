"""
This module converts messages from WhatsApp to an internal representation,
so that multiple WhatsApp chats (even from different persons) can be combined
into one single output.
"""

import re
from shutil import copyfile
from datetime import datetime

# Relevant for files
FILE_DIRECTORY = 'chats'
FILENAME_INPUT = FILE_DIRECTORY + '/' + 'chat2.txt'
FILENAME_DATA = FILE_DIRECTORY + '/' + 'messages'

# Relevant for message format
NAMES = {'Iris': ['Iris Bergers'], 'Rens': ['Rens Oliemans']}
FORMATS = ['%d-%m-%y, %H:%M', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y, %H:%M', '%m/%d/%y, %H:%M']
# The \< and 3 are for the person name
PATTERN = r"(?P<date>(\S| )+) - (?P<person>(\w|\<|3| )+): (?P<message>(\S| )+)"
message_prog = re.compile(PATTERN)


def update_messages():
    backup_files()

    with open(FILENAME_DATA) as f:
        messages = set([parse_message(row) for row in f])
    new_messages = get_new_messages()
    messages = messages.union(new_messages)

    with open(FILENAME_DATA, 'w') as f:
        for message in messages:
            f.write(str(message) + '\n')

    print(len(messages))


def backup_files():
    copyfile(FILENAME_DATA, FILENAME_DATA + '.bak')
    copyfile(FILENAME_INPUT, FILENAME_INPUT + '.bak')


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


def get_new_messages():
    messages = set()
    with open(FILENAME_INPUT) as f:
        for row in list(f):
            message = parse_message(row)
            if message is None:
                continue

            message = replace_names(message)
            messages.add(message)
    return messages


def replace_names(message):
    if message.person in NAMES.keys():
        return message
    else:
        for key in NAMES:
            if message.person in NAMES[key]:
                message.person = key
                return message


class Message:

    def __init__(self, date_time, person, message):
        self.date_time = date_time
        self.person = person
        self.message = message

    def __hash__(self):
        # This is in so that two messages with the same time will be only added
        # to a set once. This is so that if two people with different settings
        # (resulting in different self.person values) import their chat file,
        # the messages will still only be counted once
        return int(self.date_time.timestamp())

    def __eq__(self, other):
        return hash(self) == hash(other) and type(other) == type(self)

    def __str__(self):
        return f"{self.date_time}--{self.person}--{self.message}"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self.date_time, self.person, self.message

    def __lt__(self, other):
        return self.date_time < other.date_time


if __name__ == '__main__':
    update_messages()
