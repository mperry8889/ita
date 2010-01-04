import unittest
from scrabble import scrabble

class test_(unittest.TestCase):

    EXAMPLE_WORDLIST = ['azotised', 'bawdiest', 'dystocia',
                        'geotaxis', 'iceboats', 'oxidates',
                        'oxyacids', 'sweatbox', 'tideways']
    EXAMPLE_LETTERS = ['w', 'g', 'd', 'a', 's', 'x', 'z', 'c', 
                       'y', 't', 'e', 'i', 'o', 'b']

    def test_simple(self):
        """Simple example"""
        words = scrabble(["xyz"], ['x', 'y', 'z'])
        self.assertTrue(words == ["xyz"])

    def test_example(self):
        """Example that was given on the sheet"""
        words = scrabble(self.EXAMPLE_WORDLIST, self.EXAMPLE_LETTERS)
        self.assertTrue(len(words) == len(self.EXAMPLE_WORDLIST))
        for word in words:
            self.assertTrue(word in self.EXAMPLE_WORDLIST)
        
    def test_duplicates_simple(self):
        """Example with duplicate letters"""
        words = scrabble(['aa', 'bb'], ['a', 'a', 'b', 'b'])
        self.assertTrue(len(words) == 2)
        self.assertTrue('aa' in words)
        self.assertTrue('bb' in words)

    def test_duplicates_negative(self):
        """Negative example with duplicate letters"""
        words = scrabble(['aaa', 'bbb'], ['a', 'a', 'b', 'b'])
        self.assertTrue(len(words) == 0)

    def test_duplicates_other(self):
        """"Another negative example with duplicates"""
        words = scrabble(['xyzz'], ['x', 'y', 'z'])
        self.assertTrue(len(words) == 0)

if __name__ == "__main__":
    unittest.main()
