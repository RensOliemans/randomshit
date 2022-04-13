import unittest

from main import group


class TestMessageGrouper(unittest.TestCase):
    def test_simple_message(self):
        message = """23/01/2022, 13:16 - Vicky: Wordle 218 3/6

⬛⬛⬛⬛⬛
🟨🟩🟩🟨⬛
🟩🟩🟩🟩🟩
"""
        grouped = group(lines)
        self.assertEqual(message, grouped)


if __name__ == "__main__":
    unittest.main()
