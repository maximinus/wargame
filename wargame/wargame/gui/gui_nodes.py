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
    def __init__(self, rect, image, align=Align.NONE, fill=False):
        # align is for when a parent decides that the area allocated to a GUI widget
        # is smaller than the area to draw to. In all cases, the parent widget will
        # render any outside area. This flag will override the parent alignment
        # unless set to Align.NONE
        # fill tells parent that it will consume all the space it can
        self.align = align
        self.fill = fill
        super().__init__(rect, image)

    @property
    def minimum_size(self):
        # return the space that this widget would like to consume
        # returns a 3-value tuple: [width, height, bool(fill)]
        return [self.image.get_width(), self.image.get_height(), self.fill]


class VerticalContainer(GuiNode):
    """
    Contains nodes displayed vertically
    A container needs TWO align values.
    The standard align is to override the parent align if space is more than required
    The align_children setting is how to aling the child nodes
    """
    def __init__(self, nodes, background, border=4, align=Align.NONE, align_children=Align.CENTRE_LEFT, fill=False):
        self.nodes = nodes
        self.border = border
        self.background = background
        self.align = align
        self.align_children = align_children
        self.fill = fill
        image = self.build_image()
        rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        super().__init__(rect, image, align=self.align, fill=self.fill)

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
        return [width, height, self.fill]

    def update(self, time_delta):
        pass

    def draw_single_dirty(self, rect, screen):
        pass

    def handle(self, message):
        # iterate through nodes in the container
        for i in self.nodes:
            if i.handle(message):
                # handled and blocked by something
                return True
        # message may be passed on to other nodes
        return False

    def build_image(self):
        # get all the node images
        width, height, fill = self.minimum_size
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
