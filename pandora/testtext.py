import unittest


from textpuzzle import evalue, wvalue, svalue, text

given_elements = {'He': 2, 'O': 3, 'I': 1, 'a': 0}
given_words = {'Hello': 5, 'Listen': 13, 'Carefully': 8, 'So': 7, 'Will': 6, 'Tell': 5, 'You': 4, 'Short': 5, 'Story': 8, 'With': 7, 'Hidden': 5, 'Meaning': 7}


class TestEvalue(unittest.TestCase):

    def test_given_elements(self):
        for element in given_elements.keys():
            self.assertEqual(evalue(element), given_elements[element])

    def test_hello(self):
        self.assertEqual(wvalue('Hello', debug=False), 5)

    def test_listen(self):
        self.assertEqual(wvalue('Listen', debug=False), 13)

    def test_carefully(self):
        self.assertEqual(wvalue('carefully', debug=False), 8)

    def test_so(self):
        self.assertEqual(wvalue('so', debug=False), 7)

    def test_will(self):
        self.assertEqual(wvalue('will', debug=False), 6)

    def test_tell(self):
        self.assertEqual(wvalue('tell', debug=False), 5)

    def test_you(self):
        self.assertEqual(wvalue('you', debug=False), 4)

    def test_short(self):
        self.assertEqual(wvalue('short', debug=False), 5)

    def test_story(self):
        self.assertEqual(wvalue('story', debug=False), 8)

    def test_with(self):
        self.assertEqual(wvalue('with', debug=False), 7)

    def test_hidden(self):
        self.assertEqual(wvalue('hidden', debug=False), 5)

    def test_meaning(self):
        self.assertEqual(wvalue('meaning', debug=False), 7)


if __name__ == '__main__':
    unittest.main()
