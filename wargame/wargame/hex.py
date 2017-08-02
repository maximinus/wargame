#!/usr/bin/env python3

# a simple hex


class HexVector:
    """
    Hex vector for q and r
    """
    def __init__(self, q, r):
        self.q = q
        self.r = r


NEXT_HEX_ODD = [HexVector(1, 0), HexVector(0, -1),
                HexVector(-1, -1), HexVector(-1, 0),
                HexVector(-1, 1), HexVector(0, 1)]

NEXT_HEX_EVEN = [HexVector(1, 0), HexVector(1, -1),
                 HexVector(0, -1), HexVector(-1, 0),
                 HexVector(0, 1), HexVector(1, 1)]


HEX_SIZE = 64


class HexPosition:
    """
    An object to represent a hexes position
    """
    def __init__(self, q, r):
        self.q = q
        self.r = r

    @property
    def s(self):
        return -self.q - self.r

    @property
    def pixel_position(self):
        x = HEX_SIZE * self.q + (32 * self.r)
        y = HEX_SIZE * self.r - (16 * self.r)
        return (x, y)

    def __repr__(self):
        return '({0}, {1})'.format(self.q, self.r)


class Hex(HexPosition):
    def __init__(self, q, r):
        super().__init__(q, r)

    def __repr__(self):
        return 'Hex at {0}'.format(self.pixel_position)
