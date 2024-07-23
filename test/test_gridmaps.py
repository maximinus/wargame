import unittest

from wargame.nodes.gridmap import make_rectangle


class TestRectangleGridHexes(unittest.TestCase):
    def test_single_hex(self):
        hexes = make_rectangle(1, 1, 50)
        self.assertTrue(len(hexes) == 1)

    def test_multiple_hexes(self):
        hexes = make_rectangle(5, 5, 50)
        self.assertTrue(len(hexes) == 25)

    def test_radius_correct(self):
        hexes = make_rectangle(1, 1, 50)
        self.assertEqual(hexes[0].radius, 50)

    def test_single_hex_at_origin(self):
        hexes = make_rectangle(1, 1, 50)
        self.assertEqual(hexes[0].position.q, 0)
        self.assertEqual(hexes[0].position.r, 0)
