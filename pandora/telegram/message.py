import datetime
from collections import namedtuple

class Puzzle:

    def __init__(self, number, team, timestamp):
        self.number = number
        self.team = team
        self.timestamp = self.parse_stamp(timestamp)

    def parse_stamp(self, timestamp):
        return timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __str__(self):
        return '{} solved {} at {}'.format(self.team, self.number, self.timestamp)

    def __repr__(self):
        return str(self)
