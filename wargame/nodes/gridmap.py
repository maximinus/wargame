import pygame.draw

from node import Node

# a gridmap is a collection of hexes or squares to be displayed
# for now, it just holds some hexagons


class GridMap(Node):
    def __init__(self, hexes):
        self.hexes = hexes

    def render(self, surface):
        for i in self.hexes:
            pygame.draw.aalines(surface, (0, 0, 0), True, i.get_points())
