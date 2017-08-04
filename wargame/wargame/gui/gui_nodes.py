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

    def update(self, time_delta):
        pass

    def draw_single_dirty(self, rect, screen):
        pass

    @property
    def minimum_size(self):
        # return the space that this widget would like to consume
        # returns a 3-value tuple: [width, height, bool(fill)]
        return [self.image.get_width(), self.image.get_height(), self.fill]

    @staticmethod
    def from_image(image, **kwargs):
        """
        Construct a GUI node given a plain image
        (All gui nodes have an image, so this is just the simplest gui node possible)
        """
        rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        return GuiNode(rect, image, **kwargs)


class GuiContainer(GuiNode):
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

    def handle(self, message):
        # iterate through nodes in the container
        for i in self.nodes:
            if i.handle(message):
                # handled and blocked by something
                return True
        # message may be passed on to other nodes
        return False

    def build_image(self, width=0, height=0):
        if width == 0:
            # no need to account for spacing
            return self.build_simple_image()
        return self.build_simple_image()


class VerticalContainer(GuiContainer):
    """
    Contains nodes displayed vertically
    A container needs TWO align values.
    The standard align is to override the parent align if space is more than required
    The align_children setting is how to aling the child nodes
    """
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

    def build_simple_image(self):
        # we should be the minimum size at least
        width, height, fill = self.minimum_size
        image = pygame.Surface((width, height)).convert()
        # fill with background colour
        image.fill(self.background)
        # now draw the nodes. Account for the border
        ypos = self.border
        xpos = self.border
        # this is the size of the largest widget
        max_width = width - (2 * self.border)
        for i in self.nodes:
            widget_xpos = xpos
            # we know the images will fit vertically, but they may differ horizontally
            # is the image smaller?
            if i.image.get_width() < max_width:
                # either it goes to the left, centre or None. First let's ask the widget
                if i.align != Align.NONE:
                    widget_align = i.align
                else:
                    widget_align = self.align_children
                direction = Align.horizontal(widget_align)
                if direction == Align.RIGHT:
                    widget_xpos += max_width - i.image.get_width()
                elif direction == Align.CENTRE:
                    widget_xpos += (max_width - i.image.get_width()) // 2
                # if left, we don't need to do anything
            image.blit(i.image, (widget_xpos, ypos))
            ypos += i.image.get_height() + (self.border * 2)
        return image


class HorizontalContainer(GuiContainer):
    @property
    def minimum_size(self):
        images = [x.image for x in self.nodes]
        # get the total width and maximum height
        width = sum([x.get_width() for x in images])
        height = max([x.get_height() for x in images])
        width += max(len(self.nodes) - 1, 0) * (self.border * 2)
        # add the border
        width += self.border * 2
        height += self.border * 2
        return [width, height, self.fill]

    def build_simple_image(self):
        width, height, fill = self.minimum_size
        image = pygame.Surface((width, height)).convert()
        # fill with background colour
        image.fill(self.background)
        # draw nodes, accounting for the border
        xpos = self.border
        ypos = self.border
        max_height = height - (2 * self.border)
        for i in self.nodes:
            widget_ypos = ypos
            if i.image.get_height() < max_height:
                # where do we go?
                if i.align != Align.NONE:
                    widget_align = i.align
                else:
                    widget_align = self.align_children
                direction = Align.vertical(widget_align)
                if direction == Align.BOTTOM:
                    widget_ypos += max_height - i.image.get_height()
                elif direction == Align.CENTRE:
                    widget_ypos += (max_width - i.image.get_width()) // 2
            image.blit(i.image, (xpos, widget_ypos))
            xpos += i.image.get_width() + (self.border * 2)
        return image
