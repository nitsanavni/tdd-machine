import unittest
from gol import cell_dies

class TestGameOfLife(unittest.TestCase):

    def test_cell_with_less_than_two_neighbours_dies(self):
        self.assertTrue(cell_dies(1))

