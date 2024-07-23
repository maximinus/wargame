import math

import pygame.draw
from pygame import Vector2

from wargame.nodes import Node
from wargame.nodes.tiles import Axial, PointyHexagon, FlatHexagon

# a gridmap is a collection of hexes or squares to be displayed
# for now, it just holds some hexagons


def make_rectangle(width, height, radius, pointy=True):
    # returns a grid centered on Axial(0,0)
    top = -(height // 2)
    # +1 allows to be in centre
    left = -(width / 2.0) + 1
    hexes = []
    # iterate over rows
    for y in range(height):
        # and then through the columns
        for x in range(width):
            # every 2 rows, decrease left by 2
            axial_pos = Axial(math.floor(left) + x, top + y)
            if pointy:
                new_hex = PointyHexagon(axial_pos, radius)
            else:
                new_hex = FlatHexagon(axial_pos, radius)
            hexes.append(new_hex)
        left += 0.5
    return hexes


class GridMap(Node):
    def __init__(self, pos, width, height, radius, pointy=True):
        super().__init__(pos)
        self.hexes = make_rectangle(width, height, radius, pointy)
        self.hex_radius = radius
        self.grid_size = Vector2(width, height)

    @property
    def size(self):
        return Vector2((self.hex_radius * 2) * self.grid_size.x,
                       (self.hex_radius * 2) * self.grid_size.y)

    def get_surface(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

    def render(self):
        if self.surface is not None:
            return
        self.get_surface()
        for i in self.hexes:
            pygame.draw.aalines(self.surface, (0, 0, 0), True, i.get_points())
