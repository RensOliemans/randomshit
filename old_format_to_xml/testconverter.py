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

    def test_regular_movie(self):
        lines = movielines[1:6]  # whiplash movie
        movie = parse_single(lines)
        expected = correctly_build_movie(lines)
        self.assertEqual(movie, expected)

    def test_movie_without_file(self):
        lines = movielines[6:10]
        movie = parse_single(lines)
        expected = correctly_build_movie(lines)
        self.assertEqual(movie, expected)


class TestMultipleMovies(unittest.TestCase):

    def test_two_movies(self):
        lines = movielines[1:10]
        movies = parse_multiple(lines)
        expected1 = correctly_build_movie(movielines[1:6])
        expected2 = correctly_build_movie(movielines[6:10])
        self.assertEqual(movies, [expected1, expected2])

    def test_series(self):
        lines = movielines[11:25]
        movies = parse_multiple(lines)
        expected1 = correctly_build_movie(movielines[11:16])
        expected2 = correctly_build_movie(movielines[16:21])
        expected3 = correctly_build_movie(movielines[21:25])
        self.assertEqual(movies, [expected1, expected2, expected3])

    def test_movies_and_series(self):
        lines = movielines[1:25]
        movies = parse_multiple(lines)
        expected1 = correctly_build_movie(movielines[1:6])
        expected2 = correctly_build_movie(movielines[6:10])
        expected3 = correctly_build_movie(movielines[11:16])
        expected4 = correctly_build_movie(movielines[16:21])
        expected5 = correctly_build_movie(movielines[21:25])
        expected = [expected1, expected2, expected3, expected4, expected5]
        self.assertEqual(movies, expected)


def correctly_build_movie(lines):
    title, duration = parse_first_line(lines[0])
    movie = Movie(title, duration)
    for line in lines[1:]:
        movie = parse_movie_information(movie, line)
    return movie


movielines = '''films:
    Whiplash                            1h49m
        file://///130.89.168.233/Movies/Whiplash%20%282014%29/
        8.6, 94%    http://www.rottentomatoes.com/m/whiplash_2014/
        8.5         http://www.imdb.com/title/tt2582802/
        self:
    Bridge of Spies                     2h15m
        7.8, 91%    http://www.rottentomatoes.com/m/bridge_of_spies/
        7.6         http://www.imdb.com/title/tt3682448/
        self:
    The Godfather (series)              (9h5m)
        The Godfather 1                 2h55m
            file://130.89.166.148/Movies/1080p/The.Godfather.1972.1080p.BluRay.DTS.x264-ESiR/
            9.2, 99%    http://www.rottentomatoes.com/m/godfather/
            9.2         http://www.imdb.com/title/tt0068646/
            self:
        The Godfather 2                 3h20m
            file://130.89.166.148/Movies/1080p/The.Godfather.Part.II.1974.1080p.BluRay.DTS.x264-ESiR/
            9.5, 97%    http://www.rottentomatoes.com/m/godfather_part_ii/?search=the%20godfather%202
            9.0         http://www.imdb.com/title/tt0071562/
            self:
        The Godfather 3                 2h50m
            file://130.89.166.148/Movies/1080p/The.Godfather.Part.III.1990.1080p.BluRay.DTS.x264-ESiR/
            6.4, 67%    http://www.rottentomatoes.com/m/godfather_part_iii/
            7.6         http://www.imdb.com/title/tt0099674/'''.split('\n')


if __name__ == '__main__':
    unittest.main()
