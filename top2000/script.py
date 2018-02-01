import sys
import pandas as pd


def parse_excel(filename):
    COLNAME = 'pos 2017'
    xls = pd.ExcelFile(filename)
    sheet0 = xls.parse(0)
    pos = sheet0[COLNAME]
    titles = sheet0['titel']
    artists = sheet0['artiest']
    position, title, artist = None, None, None
    songs = list()
    for index, song in enumerate(pos):
        try:
            position = int(song)
            title = titles[index]
            artist = artists[index]

            songs.append(Song(title, artist, position, None))
            if type(artist) == float:
                print("Index:{}\tPosition:{}\tSong:{}\tArtist:{}"
                      .format(index, position, song, artist))
        except:
            # row isn't a song, has no pos variable
            pass

    return songs


def main():
    # filename = 'songs'
    filename = 'TOP-2000-2017.xls'
    # songs = get_songs(filename)
    songs = parse_excel(filename)

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
                print("Artist {} has {} entries"
                      .format(artist, len(artist_songs)))
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
                amount = int(input("Amount:\t"))
                top_artists, top_songs = maximum(songs, amount)
                print(top_artists)
                print(print_songs(top_songs))
            elif choice == "list":
                for song in songs:
                    print(song)
            elif choice == "pos":
                pos = int(input("Position:\t"))
                print(songs[::-1][pos - 1])
    except KeyboardInterrupt:
        print("Cancelled program")
        sys.exit(0)


def print_songs(songs):
    song_string = ""
    for song in songs:
        song_string += str(song) + "\n"
    return song_string


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
        if title.lower() in song.title.lower():
            correct_song.append(song)
    return correct_song


def maximum(songs, amount=1):
    return top_artists(songs, amount), top_songs(songs, amount)


def top_songs(songs, amount=1):
    return songs[-amount:]


def top_artists(songs, amount=1):
    artists = artists_dict(songs)
    # sorted artists
    sorted_artists = sorted(artists,
                            key=lambda key: artists[key])[-amount:][::-1]
    end_dict = dict()
    for artist in sorted_artists:
        end_dict[artist] = artists[artist]
    return end_dict


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


class Song():
    def __init__(self, title, artist, position, year):
        self.title = title
        self.artist = artist
        self.position = position
        self.year = year

    def __str__(self):
        return ("{pos}\t{title:20}\t{artist:20}\t{year}"
                .format(pos=self.position, title=self.title,
                        artist=self.artist, year=self.year))

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    main()
