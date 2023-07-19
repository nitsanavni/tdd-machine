import unittest
from fizzbuzz import fizzbuzz
class FizzBuzzTest(unittest.TestCase):
    def test_fizzbuzz_of_1_is_1(self):
        self.assertEqual(fizzbuzz(1), 1)
if __name__ == '__main__':
    unittest.main()
