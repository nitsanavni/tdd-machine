import unittest
from fizzbuzz import fizzbuzz
class TestFizzBuzz(unittest.TestCase):
    def test_number(self):
        self.assertEqual(fizzbuzz(2), 2)
    def test_fizz(self):
        self.assertEqual(fizzbuzz(3), 'Fizz')
    def test_buzz(self):
        self.assertEqual(fizzbuzz(5), 'Buzz')
    def test_fizzbuzz(self):
        self.assertEqual(fizzbuzz(15), 'FizzBuzz')
if __name__ == '__main__':
    unittest.main()
