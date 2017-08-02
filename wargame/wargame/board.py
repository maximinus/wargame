#!/usr/bin/env python3

import pygame

from wargame.hex import Hex
from wargame.loader import Resources
from wargame.node import Node


class GameBoard(Node):
    def __init__(self, rect, hex_width, hex_height):
        super().__init__(rect)
        self.hexes = []
        self.build_map(hex_width, hex_height)
        self.build_display()

    def build_map(self, width, height):
        self.hexes = []
        for r in range(0, height):
            r_offset = r // 2
            for q in range(-r_offset, width - r_offset):
                self.hexes.append(Hex(q, r))

    def build_display(self):
        hex_image = Resources.get_hex('green')
        self.image = pygame.Surface((400, 300)).convert()
        for i in self.hexes:
            self.image.blit(hex_image, i.pixel_position)

    def __repr__(self):
        return '<GameMap> at {0}'.format(self.rect)
