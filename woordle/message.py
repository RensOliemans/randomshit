from datetime import date
from dataclass import dataclass


@dataclass
class Message:
    date: date
    person: str
    game: str
    number: int
    score: float
