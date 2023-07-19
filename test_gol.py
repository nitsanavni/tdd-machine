import unittest
from gol import cell_dies, lives_on, dies_from_overpopulation, becomes_live
class TestGameOfLife(unittest.TestCase):
    def test_cell_with_less_than_two_neighbours_dies(self):
        self.assertTrue(cell_dies(1))
    def test_cell_with_two_or_three_neighbours_lives_on(self):
        self.assertTrue(lives_on(2))
    def test_cell_with_more_than_three_neighbours_dies(self):
        self.assertTrue(dies_from_overpopulation(4))
    def test_dead_cell_with_three_live_neighbours_becomes_live(self):
        self.assertTrue(becomes_live(3))


