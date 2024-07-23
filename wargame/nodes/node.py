import pygame
from pygame import Vector2


class Node:
    def __init__(self, pos):
        self.position = pos
        self.surface = None
        self.centered = True

    def get_surface(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

    def render(self):
        # render node to its own surface
        pass

    @property
    def size(self):
        return Vector2(1, 1)

    @property
    def dirty(self):
        return self.surface is None

    @property
    def container(self):
        # does this node contain children?
        return False

    @property
    def children(self):
        # return the children of this node
        return []
