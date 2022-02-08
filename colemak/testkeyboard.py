import unittest

from keyboard import get_movements, distance, distances, KEYBOARD_COLEMAK


class TestDistanceMethod(unittest.TestCase):
    def setUp(self):
        self.movements = get_movements(KEYBOARD_COLEMAK)

    def test_zero_distance(self):
        self.assertEqual(distance("arstneio", self.movements), 0)
        self.assertEqual(distance("aasstrstneo", self.movements), 0)
        self.assertEqual(distance("", self.movements), 0)

    def test_regular_distance(self):
        self.assertEqual(distance("word", self.movements), 2)
        self.assertEqual(distance("qwerty", self.movements), 3)

    def test_corner_distance(self):
        self.assertEqual(distance("great", self.movements), 2)
        self.assertEqual(distance("kbdhgj", self.movements), 10)

    def test_same_letter_distance(self):
        self.assertEqual(distance("qq", self.movements), 1)
        self.assertEqual(distance("apps", self.movements), 1)
        self.assertEqual(distance("fppffwfww", self.movements), 6)
        self.assertEqual(distance("kkbbddhhggjj", self.movements), 10)


class TestDistancesMethod(unittest.TestCase):
    def setUp(self):
        self.movements = get_movements(KEYBOARD_COLEMAK)

    def test_general_distances(self):
        expected = {"great": 2}
        self.assertEqual(distances(["great"], self.movements), expected)
        expected = {"kbdhgj": 10, "great": 2}
        self.assertEqual(distances(["kbdhgj", "great"], self.movements), expected)


if __name__ == "__main__":
    unittest.main()
