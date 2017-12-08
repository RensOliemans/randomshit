import re
import json

indent_level = 4


class Movie(object):
    def __init__(self, title="", duration="", file_url="", tomatoes="", imdb=None, rating=None, part_of_serie=False):
        self.title = title
        self.duration = duration
        self.file_url = file_url
        self.tomatoes = tomatoes
        self.imdb = imdb
        self.rating = rating
        self.part_of_serie = part_of_serie

    def __str__(self):
        return "{} - {}".format(self.title, self.duration)

    def __repr__(self):
        return str(self)


class Tomatoes(object):
    def __init__(self, rating, percentage, url):
        self.rating = rating
        self.percentage = percentage
        self.url = url

    def __str__(self):
        return "{} - {}, at {}".format(self.rating, self.percentage, self.url)

    def __repr_(self):
        return "{} - {}, at {}".format(self.rating, self.percentage, self.url)


class IMDB(object):
    def __init__(self, rating, url):
        self.rating = rating
        self.url = url

    def __str__(self):
        return "{}, at {}".format(self.rating, self.url)

    def __repr_(self):
        return "{}, at {}".format(self.rating, self.url)


def parse_first_line(line):
    wordList = re.sub("[^\w]", " ", line).split()
    movie_title = ""
    duration = ""
    for i, word in enumerate(wordList):
        if i == len(wordList) - 1:
            duration = word
            break
        movie_title += word + " "
    return movie_title[:-1], duration


def parse_tomato_line(line):
    # file is like this: "x, y    z"
    # x = rating, y = percentage, z = url
    first = line.split(", ")
    second = first[1].split("    ")

    rating = first[0].strip()
    percentage = second[0].strip()
    url = second[1].strip()
    return Tomatoes(rating, percentage, url)


def parse_imdb_line(line):
    # file is like this: "x         z"
    # x = rating, z = url
    splitted = line.split("         ")
    rating = splitted[0].strip()
    url = splitted[1].strip()
    return IMDB(rating, url)


def parse_movie_information(current_movie, line):
    is_file_line = "file://" in line
    is_tomato_line = "rottentomatoes.com" in line
    is_imdb_line = "imdb.com" in line
    if is_file_line:
        current_movie.file_url = line.strip()
    elif is_tomato_line:
        current_movie.tomatoes = parse_tomato_line(line)
    elif is_imdb_line:
        current_movie.imdb = parse_imdb_line(line)
    else:
        try:
            current_movie.rating = float(line.split("self: ")[1])
        except (IndexError, ValueError):
            # movie has no rating
            current_movie.rating = None
    return current_movie


def go_over_lines(filename="movies.txt"):
    movies = list()
    with open(filename) as f:
        current_movie = Movie()
        is_serie = False
        for line in f:
            amount_of_spaces = len(line) - len(line.lstrip())
            level = amount_of_spaces // indent_level
            if level == 1:
                # contains a movie or series
                is_serie = "series" in line
                if is_serie:
                    pass
                else:
                    # first store the current movie, since we now have a new movie
                    movies.append(current_movie)
                    # then, parse the new movie
                    current_movie = Movie()
                    current_movie.title, current_movie.duration = parse_first_line(line)

            elif level == 2:
                if is_serie:
                    movies.append(current_movie)
                    current_movie = Movie()
                    current_movie.title, current_movie.duration = parse_first_line(line)
                else:
                    # contains the information about a movie
                    current_movie = parse_movie_information(current_movie, line)
            elif level == 3:
                # contains the information about a movie
                current_movie = parse_movie_information(current_movie, line)

    return movies[1:]
