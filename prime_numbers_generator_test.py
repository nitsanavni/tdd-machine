import unittest
from prime_numbers_generator import prime_numbers_generator

class PrimeNumbersGeneratorTest(unittest.TestCase):
    def test_prime_numbers_generator(self):
        self.assertEqual(prime_numbers_generator(10), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

if __name__ == '__main__':
    unittest.main()
    def test_prime_numbers_generator_corner_cases(self):
        self.assertEqual(prime_numbers_generator(0), [])
        self.assertEqual(prime_numbers_generator(1), [2])
