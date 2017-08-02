#!/usr/bin/env python3

import pygame

from wargame.nodes import ImageNode
from wargame.gui.layout import Align


# all nodes need a minimum_size value
# we need 2 calls
# 1: how much room do you need at a minimum
# 2: draw your image with this much room
# gien it's an array, then we go and ask each item how
# much size it needs, and if it wants to fill


class GuiNode(ImageNode):
    def __init__(self, rect, image):
        self.align = Align.LEFT
        super().__init__(rect, image)


class VerticalContainer(GuiNode):
    """
    Contains nodes displayed vertically
    """
    def __init__(self, nodes, background, border=4, align=Align.LEFT, fill=False):
        self.nodes = nodes
        self.border = border
        self.background = background
        self.fill = fill
        self.align = align
        image = self.build_image()
        rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        super().__init__(rect, image)

    @property
    def minimum_size(self):
        images = [x.image for x in self.nodes]
        # get the maximum width and total height
        width = max([x.get_width() for x in images])
        height = sum([x.get_height() for x in images])
        height += max(len(self.nodes) - 1, 0) * (self.border * 2)
        # add the border
        width += self.border * 2
        height += self.border * 2
        return (width, height)

    def update(self, time_delta):
        pass

    def draw_single_dirty(self, rect, screen):
        pass

    def handle(self, message):
        # iterate through nodes in the container
        for i in self.nodes:
            i.handle(message)

    def build_image(self):
        # get all the node images
        width, height = self.minimum_size
        image = pygame.Surface((width, height)).convert()
        # fill with background colour
        image.fill(self.background)
        # now draw the nodes. Account for the border
        ypos = self.border
        xpos = self.border
        for i in self.nodes:
            image.blit(i.image, (xpos, ypos))
            ypos += i.image.get_height() + (self.border * 2)
        return image
