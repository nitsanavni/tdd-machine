import unittest
from fizzbuzz import fizzbuzz
class TestFizzBuzz(unittest.TestCase):
    def test_fizzbuzz(self):
        self.assertEqual(fizzbuzz(3), 'Fizz')
        self.assertEqual(fizzbuzz(5), 'Buzz')
        self.assertEqual(fizzbuzz(15), 'FizzBuzz')
        self.assertEqual(fizzbuzz(2), '2')
if __name__ == '__main__':
    unittest.main()
