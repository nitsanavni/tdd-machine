from fizzbuzz import fizzbuzz


import unittest


class TestFizzBuzz(unittest.TestCase):


    def test_fizzbuzz(self):


        self.assertEqual(fizzbuzz(1),'1')
