#!/usr/bin/env python3

import pygame

from wargame.nodes import ImageNode
from wargame.loader import Resources
from wargame.gui.helpers import add_border


class BorderWidget(ImageNode):
    """
    A border widget is a widget that contains something (like a window)
    It must handle setting the x/y coords relative to itself
    """
    border_config = 'WindowBorder'

    def __init__(self, contents, xpos=-1, ypos=-1):
        self.container = contents
        # get the contents to render themselves
        self.container.build_image()
        border = Resources.configs.get(self.border_config)
        image = self.build_widget_display(border, self.container.image)
        if xpos < 0:
            xpos, ypos = Resources.get_centre(image.get_width(), image.get_height())
        rect = pygame.Rect(xpos, ypos, image.get_width(), image.get_height())
        super().__init__(rect, image)

    def update(self, time_delta):
        pass

    def draw_single_dirty(self, rect, screen):
        pass

    def draw_dirty(self, rect, scene):
        pass

    def handle(self, message):
        # pass the message to the container object, unless we
        # want to do something with this message first
        self.container.handle(message)

    def build_widget_display(self, border, base_image):
        self.container.build_image()
        image = add_border(base_image, border, Resources.get_image(border.image))
        # only relative to the window
        # have to add widths and border
        print(border.dimensions['extra_height'])
        print(border.dimensions.extra_width)
        border_size = border.border_size
        deltax = border.dimensions.extra_width + border_size
        deltay = border.dimensions.extra_height + border_size
        self.container.update_position(deltax, deltay)
        return image

    def build_image(self):
        pass


class Window(BorderWidget):
    """
    A gui widget with the border of a window
    """
    border_config = 'WindowBorder'
