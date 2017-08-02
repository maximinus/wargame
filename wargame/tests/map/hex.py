#!/usr/bin/env python3

import unittest
from game_map.hex import HexPosition, HexVector


class HexPositionTest(unittest.TestCase):
    def test_q_ok(self):
        my_hex = HexPosition(3, 0)
        self.assertEqual(my_hex.q, 3)

    def test_r_ok(self):
        my_hex = HexPosition(0, 3)
        self.assertEqual(my_hex.r, 3)

    def test_s_ok(self):
        my_hex = HexPosition(3, 3)
        self.assertEqual(my_hex.s, -6)

    def test_has_string(self):
        string = str(HexPosition(3, 3))
        self.assertTrue(isinstance(string, str))


class HexVectorTest(unittest.TestCase):
    def test_q_ok(self):
        my_hex = HexVector(3, 0)
        self.assertEqual(my_hex.q, 3)

    def test_r_ok(self):
        my_hex = HexVector(0, 3)
        self.assertEqual(my_hex.r, 3)


if __name__ == '__main__':
    unittest.main()
