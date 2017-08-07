#!/usr/bin/env python3

import pygame

from wargame.nodes import ImageNode
from wargame.loader import Resources
from wargame.gui.border import add_border


class Window(ImageNode):
    def __init__(self, contents, xpos=-1, ypos=-1):
        self.container = contents
        # get the contents to render themselves
        border = Resources.configs.get('WindowBorder')
        image = self.build_image(border, self.container.image)
        if xpos < 0:
            xpos, ypos = Resources.get_centre(image.get_width(), image.get_height())
        rect = pygame.Rect(xpos, ypos, image.get_width(), image.get_height())
        super().__init__(rect, image)

    def update(self, time_delta):
        pass

    def draw_single_dirty(self, rect, screen):
        pass

    def handle(self, message):
        # iterate through nodes in the container
        for i in self.container:
            i.handle(message)

    def build_image(self, border, base_image):
        self.container.build_image()
        return add_border(base_image, border, Resources.get_image(border.image))
