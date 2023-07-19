import unittest
import fizzbuzz

class FizzBuzzTest(unittest.TestCase):

    def test_multiple_of_3(self):
        self.assertEqual(fizzbuzz.fizzbuzz(3), 'Fizz')

if __name__ == '__main__':
    unittest.main()
