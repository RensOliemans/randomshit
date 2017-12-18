import sys


def parse_line(line):
    items = line.split('\t')
    position, title, artist, year = None, None, None, None
    try:
        position = items[0]
        title = items[1]
        artist = items[2]
        year = items[3]
    except IndexError:
        # print('Error in line "{}"'.format(line))
        return

    return Song(title, artist, position, year)


def get_choice(choices):
    choice = ""
    while choice not in choices:
        choice = input("Choose one of {}:".format(", ".join(choices)))
    return choice


def main():
    filename = 'songs'
    songs = get_songs(filename)

    try:
        while True:
            choice_set = ['artist', 'song', 'avg', 'max', 'list', 'pos']
            print("\nChoices: {}".format(choice_set))
            choice = input("Please choose\t")
            if choice == 'artist':
                artist = input("Enter artist's name:\t").lower()
                artist_songs = artist_info(songs, artist)
                for song in artist_songs:
                    print(song)
                print("Artist {} has {} entries".format(artist, len(artist_songs)))
            elif choice == 'song':
                title = input("Enter song title:\t").lower()
                correct_songs = song_info(songs, title)
                if not correct_songs:
                    print("Song not found")
                for song in correct_songs:
                    print(song)
            elif choice == "avg":
                artist = input("Enter artist's name:\t").lower()
                artist_songs = artist_info(songs, artist)
                avg = 0
                for song in artist_songs:
                    avg += int(song.position)
                if avg:
                    print("Average position: {:.2f}. Songs in list: {}"
                          .format(avg/len(artist_songs), len(artist_songs)))
                else:
                    print("Artist not found")
            elif choice == "max":
                artists = artists_dict(songs)
                top_artist = sorted(artists, key=lambda key: artists[key])[-1]
                count = artists[top_artist]
                print("Artist with most songs: {} ({} songs).\nTop song: {}"
                      .format(top_artist, count, songs[-1]))
            elif choice == "list":
                for song in songs:
                    print(song)
            elif choice == "pos":
                pos = int(input("Position:\t"))
                print(songs[::-1][pos - 1])
    except KeyboardInterrupt:
        print("Cancelled program")
        sys.exit(0)


def artist_info(songs, artist):
    artist_songs = list()
    for song in songs:
        if song is None:
            continue
        if artist == song.artist.lower():
            artist_songs.append(song)
    return artist_songs


def song_info(songs, title):
    correct_song = list()
    for song in songs:
        if song is None:
            continue
        if title.lower() == song.title.lower():
            correct_song.append(song)
    return correct_song


def maximum(songs):
    top_song = None
    artists = dict()
    top_artist = sorted(artists, key=lambda key: artists[key])[-1]
    return {top_artist: artists[top_artist]}, top_song


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


def get_songs(filename):
    f = open(filename)
    songs = list()
    for line in f:
        song = parse_line(line)
        # filter example line
        if song is None or song.year == 'jaar':
            continue
        songs.append(song)
    return songs


class Song():
    def __init__(self, title, artist, position, year):
        self.title = title
        self.artist = artist
        self.position = position
        self.year = year

    def __str__(self):
        return "{pos}\t{title:20}\t{artist:20}\t{year}".format(
                pos=self.position, title=self.title, artist=self.artist, year=self.year)

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    main()
