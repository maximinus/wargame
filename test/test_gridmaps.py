import unittest

from wargame.nodes.tiles import Axial
from wargame.nodes.gridmap import make_rectangle


class TestRectangleGridHexes(unittest.TestCase):
    def test_single_hex(self):
        hexes = make_rectangle(1, 1, 50)
        self.assertTrue(len(hexes) == 1)

    def test_multiple_hexes(self):
        hexes = make_rectangle(3, 3, 50)
        self.assertTrue(len(hexes) == 9)

    def test_radius_correct(self):
        hexes = make_rectangle(1, 1, 50)
        self.assertEqual(hexes[0].radius, 50)

    def test_single_hex_at_origin(self):
        hexes = make_rectangle(1, 1, 50)
        self.assertEqual(hexes[0].position, Axial(0, 0))

    def test_multiple_hexes_first_row(self):
        hexes = make_rectangle(3, 3, 50)
        self.assertEqual(hexes[0].position, Axial(0, 0))
        self.assertEqual(hexes[1].position, Axial(1, 0))
        self.assertEqual(hexes[2].position, Axial(2, 0))

    def test_multiple_hexes_second_row(self):
        hexes = make_rectangle(3, 3, 50)
        self.assertEqual(hexes[3].position, Axial(0, 1))
        self.assertEqual(hexes[4].position, Axial(1, 1))
        self.assertEqual(hexes[5].position, Axial(2, 1))

    def test_multiple_hexes_third_row(self):
        hexes = make_rectangle(3, 3, 50)
        self.assertEqual(hexes[6].position, Axial(-1, 2))
        self.assertEqual(hexes[7].position, Axial(0, 2))
        self.assertEqual(hexes[8].position, Axial(1, 2))
