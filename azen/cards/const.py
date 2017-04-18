SUITS = ["Diamonds", "Clubs", "Hearts", "Spades"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
          "Jack", "Queen", "King", "Ace"]

POKER_RANKS = {
    "values": {
        "Ace": 13,
        "King": 12,
        "Queen": 11,
        "Jack": 10,
        "10": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
        "Joker": 0,
    }
}

BIG2_RANKS = {
    "values": {
        "2": 13,
        "Ace": 12,
        "King": 11,
        "Queen": 10,
        "Jack": 9,
        "10": 8,
        "9": 7,
        "8": 6,
        "7": 5,
        "6": 4,
        "5": 3,
        "4": 2,
        "3": 1,
        "Joker": 0
    },
    "suits": {
        "Spades": 4,
        "Hearts": 3,
        "Clubs": 2,
        "Diamonds": 1
    }
}

DEFAULT_RANKS = {
    "values": POKER_RANKS["values"],
    "suits": BIG2_RANKS["suits"]
}

TOP = "top"
BOTTOM = "bottom"
