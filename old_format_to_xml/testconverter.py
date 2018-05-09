import unittest

from converter import Movie
from converter import parse_first_line, parse_single, parse_movie_information, parse_multiple


class TestFirstLine(unittest.TestCase):

    def test_normal_line(self):
        line = '    Whiplash                            1h49m'
        title, duration = parse_first_line(line)
        self.assertEqual(title, 'Whiplash')
        self.assertEqual(duration, '1h49m')

    def test_different_indentation(self):
        line = '        The Godfather 1                 2h55m'
        title, duration = parse_first_line(line)
        self.assertEqual(title, 'The Godfather 1')
        self.assertEqual(duration, '2h55m')

    def test_series(self):
        line = '    Kung Fu Panda (series)              (2h56m)'
        title, duration = parse_first_line(line)
        self.assertEqual(title, 'Kung Fu Panda series')
        self.assertEqual(duration, '2h56m')

    def test_watched_movie(self):
        line = "    '''The Grand Budapest Hotel'''      1h39m"
        title, duration = parse_first_line(line)
        self.assertEqual(title, 'The Grand Budapest Hotel')
        self.assertEqual(duration, '1h39m')

    def test_different_timing(self):
        line = '    Big Fish                            2h5m'
        title, duration = parse_first_line(line)
        self.assertEqual(title, 'Big Fish')
        self.assertEqual(duration, '2h5m')


class TestSingleMovie(unittest.TestCase):

    def setUp(self):
        with open('testmovies.txt') as f:
            self.lines = list(f)

    def test_regular_movie(self):
        lines = self.lines[1:6]  # whiplash movie
        movie = parse_single(lines)
        expected = correctly_build_movie(lines)
        self.assertEqual(movie, expected)

    def test_movie_without_file(self):
        lines = self.lines[6:10]
        movie = parse_single(lines)
        expected = correctly_build_movie(lines)
        self.assertEqual(movie, expected)


class TestMultipleMovies(unittest.TestCase):

    def setUp(self):
        with open('testmovies.txt') as f:
            self.lines = list(f)

    def test_two_movies(self):
        lines = self.lines[1:10]
        movies = parse_multiple(lines)
        expected1 = correctly_build_movie(self.lines[1:6])
        expected2 = correctly_build_movie(self.lines[6:10])
        self.assertEqual(movies, [expected1, expected2])

    def test_series(self):
        lines = self.lines[11:25]
        movies = parse_multiple(lines)
        expected1 = correctly_build_movie(self.lines[11:16])
        expected2 = correctly_build_movie(self.lines[16:21])
        expected3 = correctly_build_movie(self.lines[21:25])
        self.assertEqual(movies, [expected1, expected2, expected3])

    def test_movies_and_series(self):
        lines = self.lines[1:25]
        movies = parse_multiple(lines)
        expected1 = correctly_build_movie(self.lines[1:6])
        expected2 = correctly_build_movie(self.lines[6:10])
        expected3 = correctly_build_movie(self.lines[11:16])
        expected4 = correctly_build_movie(self.lines[16:21])
        expected5 = correctly_build_movie(self.lines[21:25])
        expected = [expected1, expected2, expected3, expected4, expected5]
        self.assertEqual(movies, expected)


def correctly_build_movie(lines):
    title, duration = parse_first_line(lines[0])
    movie = Movie(title, duration)
    for line in lines[1:]:
        movie = parse_movie_information(movie, line)
    return movie


if __name__ == '__main__':
    unittest.main()
