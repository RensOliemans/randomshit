"""
This module converts messages from WhatsApp to an internal representation,
so that multiple WhatsApp chats (even from different persons) can be combined
into one single output.
"""

import re
from shutil import copyfile
from datetime import datetime
import sqlite3

# Relevant for files
FILE_DIRECTORY = 'chats'
FILENAME_INPUT = FILE_DIRECTORY + '/' + 'chat-iris.txt'
FILENAME_DB = FILE_DIRECTORY + '/' + 'db.sqlite'
FILENAME_DATA = FILE_DIRECTORY + '/' + 'messages'

# Relevant for message format
NAMES = {'Iris': ['Iris Bergers', 'Iris <3'], 'Rens': ['Rens Oliemans', 'Rens']}
FORMATS = ['%d-%m-%y, %H:%M', '%d-%m-%Y %H:%M', '%Y-%m-%d %H:%M:%S',
           '%d/%m/%Y, %H:%M', '%m/%d/%y, %H:%M']
# The \< and 3 are for the person name
PATTERN = r"(?P<date>(\S| )+) - (?P<person>(\w|\<|3| )+): (?P<message>(\S| )+)"
message_prog = re.compile(PATTERN)


class MessageConverter:
    def __init__(self, dbname, filename_input):
        self._dbname = dbname
        self._input_file = filename_input

        self._conn = None

    def update_messages(self):
        self._backup_file()

        messages = self._get_new_messages()
        out = self._save_new_messages(list(messages))

        self._show_results(out)

    def _backup_file(self):
        copyfile(self._input_file, self._input_file + '.bak')

    def _get_new_messages(self):
        with open(self._input_file) as f:
            for row in f:
                message = self.parse_message(row)
                if message is None:
                    continue

                message = self.replace_names(message)
                yield message

    def _save_new_messages(self, messages):
        self._conn = sqlite3.connect(self._dbname)
        c = self._conn.cursor()

        count = c.execute('SELECT COUNT(*) FROM messages').fetchone()
        added = self._insert_messages(messages)

        go = bool(input(f'Want to add new messages? had {count}, chat contained {len(messages)} new, adding {added} '))

        if go:
            self._conn.commit()
        self._conn.close()
        return count, len(messages), added if go else 0

    def _insert_messages(self, messages):
        added = 0
        c = self._conn.cursor()
        for message in messages:
            m = (message.date_time, message.person, message.message)
            entry = c.execute('SELECT * FROM messages WHERE (date=? AND person=? AND message=?)', m).fetchone()
            if entry is None:
                c.execute('INSERT INTO messages VALUES (?, ?, ?)', m)
                added += 1

        return added

    @staticmethod
    def _show_results(out):
        count, new, added = out
        print(f'The database had {count} messages before.'
              f'The chats contained {new} messages, of which {added} were added.')

    @staticmethod
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

    @staticmethod
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

    @property
    def date(self):
        return self.date_time


if __name__ == '__main__':
    mc = MessageConverter(FILENAME_DB, FILENAME_INPUT)
    mc.update_messages()
