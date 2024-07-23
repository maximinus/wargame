import math
from pygame.math import Vector2


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

    def __repr__(self):
        return f'<Axial(q={self.q}, r={self.r}>'


class Hexagon:
    def __init__(self, position, radius):
        # we use an axial coord system:
        self.position = position
        self.radius = radius

    @property
    def center(self):
        x = self.radius * (math.sqrt(3) * self.position.q  +  math.sqrt(3) / 2.0 * self.position.r)
        y = self.radius * (1.5 * self.position.r)
        # we need to offset by the radius, so no points are negative
        return Vector2(int(x) + self.radius, int(y) + self.radius)


class PointyHexagon(Hexagon):
    def get_points(self):
        # return the points of the hexagon, from 0 degrees through 360
        pos = self.center
        points = []
        for i in range(6):
            angle = math.radians((60.0 * i) - 30.0)
            points.append(Vector2(int(pos.x + (self.radius * math.cos(angle))),
                                  int(pos.y + (self.radius * math.sin(angle)))))
        return points


class FlatHexagon(Hexagon):
    def get_points(self):
        # return the points of the hexagon, from 0 degrees through 360
        pos = self.center
        points = []
        for i in range(6):
            angle = math.radians(60.0 * i)
            points.append(Vector2(int(pos.x + (self.radius * math.cos(angle))),
                                  int(pos.y + (self.radius * math.sin(angle)))))
        return points
