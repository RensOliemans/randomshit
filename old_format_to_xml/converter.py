import re
INDENT_LEVEL = 4


class Movie(object):
    def __init__(self, title="", duration="", file_url="", tomatoes="",
                 imdb=None, rating=None, part_of_serie=False):
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
        return ("Movie. Title: {}, Duration: {}, file_url (stripped): {}, "
                "Tomato: {}. IMDB: {}. Rating: {}."
                .format(self.title, self.duration, self.file_url[10:25],
                        self.tomatoes, self.imdb, self.rating))

    def __eq__(self, other):
        return (self.title == other.title and self.duration == other.duration and
                self.file_url == other.file_url)


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
    ''' This method takes a movie and a line, and if it can, it adds new
    information from the line to the movie. It returns the movie again. '''
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


def build(lines):
    ''' This method groups certain indentation levels together'.

    Example: input: lines = ['  a', '    b', '    c', '  d', '    e']
    build(lines) will return [['  a', '    b', '    c'], ['  d', '    e']]
    '''
    groups = list()
    initial_indentation = len(lines[0]) - len(lines[0].lstrip())
    # TODO: how to name a? It's an iterator which iterates over the lines.
    a = iter(lines)
    item = next(a)

    # first group contains the first line
    group = [item]
    try:
        while True:
            item = next(a)
            indentation = len(item) - len(item.lstrip())
            if indentation == initial_indentation:
                # we reached the same indentation as the beginning, so this is
                # a new group.
                groups.append(group)
                group = [item]
            else:
                group.append(item)
    except StopIteration:
        # we reached the end of the lines, so add the 'current' group to the total
        # groups
        groups.append(group)
    return groups


def parse_single(lines):
    title, duration = parse_first_line(lines[0])
    movie = Movie(title, duration)
    for i in range(1, len(lines)):
        movie = parse_movie_information(movie, lines[i])
    return movie


def parse_multiple(lines):
    movies = list()
    groups = build(lines)
    for group in groups:
        if '(series)' in group[0]:
            # nested multiple movies, recursively call parse_multiple
            movies.extend(parse_multiple(group[1:]))
            continue
        movies.append(parse_single(group))
    return movies


def parse_total(lines):
    groups = build(lines)
    movies = groups[0][1:]
    series = groups[1][1:]
    movies = parse_multiple(movies)
    series = parse_multiple(series)
    return [movies, series]


if __name__ == '__main__':
    f = open('movies.txt')
    lines = list(f)
    print(parse_total(lines)[0])
