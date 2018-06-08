import re
from lxml import etree
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
        return f"{self.title} - {self.duration}"

    def __repr__(self):
        return (f"Movie. Title: {self.title}, Duration: {self.duration}, "
                f"file_url (stripped): {self.file_url[10:25]}, Tomato: {self.tomatoes}."
                f" IMDB: {self.imdb}. Rating: {self.rating}")

    def __eq__(self, other):
        return (self.title == other.title and self.duration == other.duration and
                self.file_url == other.file_url)


class Tomatoes(object):
    def __init__(self, rating, percentage, url):
        self.rating = rating
        self.percentage = percentage
        self.url = url

    def __str__(self):
        return f"{self.rating} - {self.percentage}, at {self.url}"

    def __repr_(self):
        return str(self)


class IMDB(object):
    def __init__(self, rating, url):
        self.rating = rating
        self.url = url

    def __str__(self):
        return f"{self.rating}, at {self.url}"

    def __repr_(self):
        return str(self)


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
    regex = r"\s*(?P<rating>\d(.\d)?)\,\s(?P<percentage>\d*\%)\s*(?P<url>\S*)"
    m = re.match(regex, line)
    rating, percentage, url = m.group('rating'), m.group('percentage'), m.group('url')
    return Tomatoes(rating, percentage, url)


def parse_imdb_line(line):
    # file is like this: "x         z"
    m = re.match(r"\s*(?P<rating>\d(.\d)?)\s*(?P<url>\S*)", line)
    rating, url = m.group('rating'), m.group('url')
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
            regex = r"self: (?P<number>\d(.\d)?)"
            current_movie.rating = float(re.findall(regex, line)[0])
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


def parse_single(lines, series=False):
    title, duration = parse_first_line(lines[0])
    movie = Movie(title, duration, part_of_serie=series)
    for i in range(1, len(lines)):
        movie = parse_movie_information(movie, lines[i])
    return movie


def parse_multiple(lines, series=False):
    movies = list()
    groups = build(lines)
    for group in groups:
        if '(series)' in group[0]:
            # nested multiple movies, recursively call parse_multiple
            movies.extend(parse_multiple(group[1:], series=True))
            continue
        movies.append(parse_single(group, series=series))
    return movies


def parse_total(lines):
    groups = build(lines)
    movies = groups[0][1:]
    series = groups[1][1:]
    movies = parse_multiple(movies)
    series = parse_multiple(series)
    return movies, series


def convert_to_xml(movies):
    page = etree.Element("Movies")
    doc = etree.ElementTree(page)
    for movie in movies:
        title = movie.title.replace(' ', '_')
        if title[0].isdigit():
            title = 'm' + title
        etree.SubElement(page, title,
                         duration=str(movie.duration),
                         tomatoes=str(movie.tomatoes),
                         imdb=str(movie.imdb))
    out_file = open('output.xml', 'wb')
    doc.write(out_file, xml_declaration=True, encoding='utf8', pretty_print=True)


if __name__ == '__main__':
    movies, series = parse_total(list(open('movies.txt')))
    # print("Movies")
    # print(*movies, sep='\n')
    convert_to_xml(movies)
