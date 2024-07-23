import pygame
from pygame import Vector2

from wargame.nodes import Node

# a scene is a collection of nodes that we draw


class Scene(Node):
    def __init__(self, nodes):
        super().__init__(Vector2(0, 0))
        self.nodes = nodes
        self.render_area = Vector2(800, 600)

    @property
    def size(self):
        return self.render_area

    def render(self):
        if self.surface is not None:
            return
        self.get_surface()
        for node in self.nodes:
            node.render()
            # blit to our texture - which is centered on (0, 0)
            if node.centered:
                base_pos = node.position - (node.size // 2) + (self.render_area // 2)
            else:
                base_pos = node.position + (self.render_area // 2)
            self.surface.blit(node.surface, base_pos)
