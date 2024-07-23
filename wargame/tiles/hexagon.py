import math


# there are 2 types of hexagon: pointy top or flat top; we will call these non-flat and flat
class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)


class Axial:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    @property
    def s(self):
        return -self.q - self.r

    @property
    def neighbors(self):
        return [Axial(self.q+1, 0), Axial(self.q+1, self.r-1), Axial(self.q, self.r-1),
                Axial(self.q-1, 0), Axial(self.q-1, self.r+1), Axial(self.q, self.r+1)]

    def distance(self, other):
        return (abs(self.q - other.q) + abs(self.q + self.r - other.q - other.r) + abs(self.r - other.r)) / 2.0


class Hexagon:
    def __init__(self, position, radius):
        # we use an axial coord system:
        self.position = position
        self.radius = radius

    @property
    def center(self):
        return Vec2(0, 0)


class PointyHexagon(Hexagon):
    def get_points(self):
        # return the points of the hexagon, from 0 degrees through 360
        pos = self.center
        points = []
        for i in range(6):
            angle = math.radians((60.0 * i) - 30.0)
            return Vec2(pos.x + (self.radius * math.cos(angle)), pos.y + (self.radius * math.sin(angle)))
