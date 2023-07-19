import unittest
from roman_numerals import to_roman

class TestRomanNumerals(unittest.TestCase):

    def test_1_returns_I(self):
        self.assertEqual(to_roman(1), "I")

if __name__ == '__main__':
    unittest.main()
    def test_5_returns_V(self):
        self.assertEqual(to_roman(5), "V")

