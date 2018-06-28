import unittest

from score import points


class TestPointMethod(unittest.TestCase):

    def test_correct_score(self):
        self.assertEqual(points((1, 1), (1, 1)), 200)
        self.assertEqual(points((0, 0), (0, 0)), 200)
        self.assertEqual(points((1, 3), (1, 3)), 200)
        self.assertEqual(points((4, 0), (4, 0)), 200)

    def test_draw(self):
        self.assertEqual(points((1, 1), (0, 0)), 100)
        self.assertEqual(points((1, 1), (3, 3)), 100)
        self.assertEqual(points((0, 0), (2, 2)), 100)

    def test_win(self):
        self.assertEqual(points((2, 1), (3, 0)), 75)
        self.assertEqual(points((1, 0), (3, 0)), 75 + 20)
        self.assertEqual(points((4, 1), (3, 1)), 75 + 20)

        self.assertEqual(points((3, 0), (2, 1)), 75)
        self.assertEqual(points((3, 0), (1, 0)), 75 + 20)
        self.assertEqual(points((3, 1), (4, 1)), 75 + 20)

    def test_goals_correct(self):
        self.assertEqual(points((0, 0), (0, 2)), 20)
        self.assertEqual(points((0, 2), (0, 0)), 20)
        self.assertEqual(points((3, 1), (1, 1)), 20)

    def test_all_wrong(self):
        self.assertEqual(points((0, 0), (2, 1)), 0)
        self.assertEqual(points((2, 1), (0, 0)), 0)
        self.assertEqual(points((2, 0), (1, 1)), 0)
        self.assertEqual(points((2, 0), (1, 5)), 0)


if __name__ == '__main__':
    unittest.main()
