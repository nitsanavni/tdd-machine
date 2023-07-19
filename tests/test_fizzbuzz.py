import unittest


class TestFizzBuzz(unittest.TestCase):

    def test_fizz(self):
        self.assertEqual(fizzbuzz(3), 'fizz')

if __name__ == '__main__':
    unittest.main()
