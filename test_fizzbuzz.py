import unittest
from fizzbuzz import fizzbuzz

class TestFizzBuzz(unittest.TestCase):
    def test_fizzbuzz(self):
        result = fizzbuzz(3)
        self.assertEqual(result, 'Fizz', f'Expected Fizz, but got {result}')
