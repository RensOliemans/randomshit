import logging
from argparse import ArgumentParser
from enum import Enum

import pandas as pd

logger = logging.Logger(__name__)


class Option(Enum):
    artist = "artist"
    song = "song"
    avg = "avg"
    max = "max"
    list = "list"
    pos = "pos"

    def __str__(self):
        return self.value


def parse_excel(filename):
    COLNAME = "pos 2017"
    xls = pd.ExcelFile(filename)
    sheet0 = xls.parse(0)
    pos = sheet0[COLNAME]
    titles = sheet0["titel"]
    artists = sheet0["artiest"]
    position, title, artist = None, None, None
    songs = list()
    for index, song in enumerate(pos):
        try:
            position = int(song)
            title = titles[index]
            artist = artists[index]

            songs.append(Song(title, artist, position))
        except ValueError as e:
            # row isn't a song, has no pos variable
            logger.debug(e)

    return songs


def main():
    # filename = 'songs'
    filename = "TOP-2000-2017.xls"
    # songs = get_songs(filename)
    songs = parse_excel(filename)
    choice = str(opts.option)

    if choice == "artist":
        artist = input("Enter artist's name:\t").lower()
        artist_songs = artist_info(songs, artist)
        print(*artist_songs, sep="\n")
        print(f"Artist {artist} has {len(artist_songs)} entries")
    elif choice == "song":
        title = input("Enter song title:\t").lower()
        correct_songs = song_info(songs, title)
        print(
            *(correct_songs) if correct_songs else "Song not found",
            sep="\n" if correct_songs else "",
        )
    elif choice == "avg":
        artist = input("Enter artist's name:\t").lower()
        artist_songs = artist_info(songs, artist)
        total = sum([song.position for song in songs if song in artist_songs])
        print(
            f"Average position: {total/len(artist_songs):.2f}. Songs in list"
            f": {len(artist_songs)}"
            if total
            else "Artist not found"
        )
    elif choice == "max":
        amount = int(input("Amount:\t"))
        artists, top_songs = top_artists(songs, amount), songs[-amount:]
        print(*artists, sep=", ")
        print(*top_songs, sep="\n")
    elif choice == "list":
        print(*songs, sep="\n")
    elif choice == "pos":
        pos = max(min(int(input("Position:\t")), 2000), 0)
        print(songs[::-1][pos - 1])


def artist_info(songs, artist):
    return [
        song for song in songs if song is not None and artist == song.artist.lower()
    ]


def song_info(songs, title):
    return [
        song
        for song in songs
        if song is not None and title.lower() in song.title.lower()
    ]


def top_artists(songs, amount=1):
    artists = artists_dict(songs)
    # sorted by value
    return sorted(artists, key=lambda key: artists[key])[-amount:][::-1]


def artists_dict(songs):
    artists = dict()
    for song in songs:
        if song is None:
            continue
        if song.artist not in artists:
            artists[song.artist] = 1
        else:
            artists[song.artist] += 1
    return artists


class Song:
    def __init__(self, title, artist, position):
        self.title = title
        self.artist = artist
        self.position = position

    def __str__(self):
        return f"{self.position}\t{self.title:20}\t{self.artist:20}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("option", type=Option, choices=list(Option))
    parser.add_argument(
        "-l",
        "--loglevel",
        dest="loglevel",
        type=str,
        help="Log level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
    )
    opts = parser.parse_args()
    logger.setLevel(opts.loglevel)
    main()
