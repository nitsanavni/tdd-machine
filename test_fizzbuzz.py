import unittest
from fizzbuzz import fizzbuzz

class TestFizzBuzz(unittest.TestCase):
    def test_fizzbuzz(self):
        self.assertEqual(fizzbuzz(3), 'Fizz')

if __name__ == '__main__':
    unittest.main()
