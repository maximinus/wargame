#!/usr/bin/env python3

import pygame

from wargame.nodes import ImageNode
from wargame.gui.layout import Align
from wargame.loader import Resources
from wargame.gui.helpers import add_border
from wargame.tweens import TweenResult

import logging
logger = logging.getLogger(__name__)

# gui objects fill their image size
# containers fill as much as they can
# containers do it one way only - but will listen to gui objects
# thus, containers have an align
# it is overridden by the gui object align


class GuiNode(ImageNode):
    def __init__(self, rect, image, align=Align.NONE, fill=False):
        # align is for when a parent decides that the area we have to fill
        # is more than the GUI widget needs. In all cases, the parent widget will
        # render any outside area. This flag will override the parent alignment
        # unless set to Align.NONE
        # fill tells parent that it will consume all the space it can
        self.align = align
        self.fill = fill
        self.offset = pygame.Rect(0, 0, 0, 0)
        super().__init__(rect, image)

    def update(self, time_delta):
        # this function requires you return a list
        # of dirty rects. In this case we have none
        return []

    def draw_single_dirty(self, rect, screen):
        pass

    def update_position(self, deltax, deltay):
        self.offset.x += deltax
        self.offset.y += deltay

    def build_image(self, width=0, height=0):
        # this function MUST be overridden.
        # to ensure no errors, we set a horrible red square
        if self.image is None:
            size = 128
            self.image = Resources.colour_surface(size, size, (255, 0, 0))
            self.rect = pygame.Rect(0, 0, size, size)
            self.visible = True

    def handle(self, message, rect):
        # returns False - we didn't consume the event
        return False

    @property
    def dirty_rects(self):
        return []

    @property
    def minimum_size(self):
        # return the space that this widget would like to consume
        return [self.image.get_width(), self.image.get_height()]

    @staticmethod
    def from_image(image, **kwargs):
        """
        Construct a GUI node given a plain image
        (All gui nodes have an image, so this is just the simplest gui node possible)
        """
        rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        return GuiNode(rect, image, **kwargs)


class GuiLabel(GuiNode):
    """
    A label is a single piece of text on one line, with a plain background
    """
    def __init__(self, text, colour, background, border=4, align=Align.NONE, fill=False):
        # we need to make a rect and an image
        # let's start with the image
        font = Resources.get_font()
        label = font.render(text, True, colour, background).convert()
        rect = pygame.Rect(0, 0, label.get_width(), label.get_height())
        if border > 0:
            width = rect.width + (2 * border)
            height = rect.height + (2 * border)
            image = pygame.Surface((width, height)).convert()
            image.fill(background)
            image.blit(label, (border, border))
            label = image
        super().__init__(rect, label, align, fill)

    def build_image(self, width=0, height=0):
        pass


class Button(GuiNode):
    """
    A gui widget with the border of a Button
    """
    border_config = 'ButtonBorder'

    def __init__(self, text, align=Align.NONE):
        # make a label of the text - but we only want the image
        label = GuiLabel(text, (0, 0, 0), (214, 214, 214)).image
        # get the contents to render themselves
        border = Resources.configs.get(self.border_config)
        image = add_border(label, border, Resources.get_image(border.image))
        rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        super().__init__(rect, image, align, False)
        self.messages = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]
        self.highlight = self.get_highlight()
        self.normal_image = self.image
        self.changed = False

    def handle(self, message, rect):
        # we need to handle a mouse move or a mousedown
        # is that what we have?
        if message.message_id not in self.messages:
            return False
        # is the mouse in the rect?
        xpos = message.data.pos[0] - (rect.x + self.offset.x)
        ypos = message.data.pos[1] - (rect.y + self.offset.y)

        if self.rect.collidepoint(xpos, ypos):
            # mouse says inside
            if self.image is self.normal_image:
                print('Inside')
                self.image = self.highlight
                self.changed = True
        else:
            if self.image is self.highlight:
                print('Outside')
                self.image = self.normal_image
                self.changed = True

    def get_highlight(self):
        highlight = self.image.copy()
        alpha = Resources.alpha_surface(self.image.get_width(), self.image.get_height(), 64)
        alpha.fill((255, 255, 255))
        highlight.blit(alpha, (0, 0))
        return highlight

    def update(self, time_delta):
        # need to pass back a list of dirty rects
        if self.changed:
            # make sure we don't update next time
            self.changed = False
            print('Updated')
            # this is a rect that is relative to this node
            return [self.rect]
        return []


class GuiImage(GuiNode):
    """
    An image is a just that, a simple image
    """
    def __init__(self, image, align=Align.NONE):
        rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        super().__init__(rect, image, align, False)

    def build_image(self):
        pass

    @staticmethod
    def from_image_node(node):
        return GuiImage(node.image)

    @staticmethod
    def from_image(image_name):
        image = Resources.get_image(image_name)
        return GuiImage(image)


class GuiContainer(GuiNode):
    """
    A container must set it's childrens x/y
    position relative to itself
    We will know the co-ords when we blit
    """
    def __init__(self, nodes, background, border=4, align_children=Align.CENTRE):
        rect = pygame.Rect(0, 0, 0, 0)
        super().__init__(rect, None, align=Align.NONE, fill=True)
        # not visible until the image has been drawn
        self.visible = False
        self.nodes = nodes
        self.border = border
        self.background = background
        self.align_children = align_children

    def handle(self, message, rect):
        # iterate through nodes in the container
        for i in self.nodes:
            if i.handle(message, rect):
                # handled and blocked by something
                return True
        # message may be passed on to other nodes
        return False

    def update_position(self, deltax, deltay):
        # need to update ourselves and all children
        self.rect.x += deltax
        self.rect.y += deltay
        for i in self.nodes:
            i.update_position(deltax, deltay)

    @property
    def minimum_size(self):
        # make sure to override this
        logger.error('GuiContainer minimum_size not overriden')
        return(0, 0, False)

    def build_image(self, width=0, height=0):
        # this routine should build the image needed to render
        # if width and height are set, we must use this width and height
        # width and height are ALWAYS large enough to handle all the nodes
        if width == 0:
            # no need to account for spacing
            image = self.build_simple_image()
        else:
            # we must fill the entire space
            image = self.build_full_image(width, height)
        self.rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        self.image = image
        return image


class VerticalContainer(GuiContainer):
    """
    Contains nodes displayed vertically
    A container needs TWO align values.
    The standard align is to override the parent align if space is more than required
    The align_children setting is how to aling the child nodes
    """
    @property
    def minimum_size(self):
        sizes = [x.minimum_size for x in self.nodes]
        # get the maximum width and total height
        width = max([x[0] for x in sizes])
        height = sum([x[1] for x in sizes])
        height += max(len(self.nodes) - 1, 0) * (self.border * 2)
        # add the border
        width += self.border * 2
        height += self.border * 2
        return [width, height, self.fill]

    def build_simple_image(self):
        # we should be the minimum size at least
        width, height, fill = self.minimum_size
        image = Resources.colour_surface(width, height, self.background)
        # now draw the nodes. Account for the border
        ypos = self.border
        xpos = self.border
        # this is the size of the largest widget
        max_width = width - (2 * self.border)
        for i in self.nodes:
            widget_xpos = xpos
            # we know the images will fit vertically, but they may differ horizontally
            # is the image smaller?
            if i.minimum_size[0] < max_width:
                # either it goes to the left, centre or None. First let's ask the widget
                if i.align != Align.NONE:
                    widget_align = i.align
                else:
                    widget_align = self.align_children
                direction = Align.horizontal(widget_align)
                if direction == Align.RIGHT:
                    widget_xpos += max_width - i.minimum_size[0]
                elif direction == Align.CENTRE:
                    widget_xpos += (max_width - i.minimum_size[0]) // 2
                # if left, we don't need to do anything
            if i.image is None:
                i.build_image()
            # now we have the xpos and ypos
            i.update_position(widget_xpos, ypos)
            image.blit(i.image, (widget_xpos, ypos))
            ypos += i.image.get_height() + (self.border * 2)
        return image

    def build_full_image(self, width, height):
        if width == -1:
            # use rect size
            width = self.minimum_size[0]
        image = Resources.colour_surface(width, height, self.background)
        # we fill the given space with the widgets.
        # what is our minimum size?
        sizes = [x.minimum_size for x in self.nodes]
        min_height = sum([x[1] for x in sizes])
        if min_height < height:
            # we have spare space, since we only worry about the vertical size
            # how do we distribute the space?
            if self.align_children == Align.TOP:
                # everything at the top
                node_image = self.build_simple_image()
                # (0,0) -> no need to update positions
                image.blit(node_image, (0, 0))
                return image
        else:
            # must be same size
            return self.build_simple_image()


class HorizontalContainer(GuiContainer):
    @property
    def minimum_size(self):
        sizes = [x.minimum_size for x in self.nodes]
        # get the total width and maximum height
        width = sum([x[0] for x in sizes])
        height = max([x[1] for x in sizes])
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
            if i.minimum_size[1] < max_height:
                # where do we go?
                if i.align != Align.NONE:
                    widget_align = i.align
                else:
                    widget_align = self.align_children
                direction = Align.vertical(widget_align)
                if direction == Align.BOTTOM:
                    widget_ypos += max_height - i.minimum_size[1]
                elif direction == Align.CENTRE:
                    widget_ypos += (max_height - i.minimum_size[1]) // 2
            if i.image is None:
                # it is another container, so we need to build the image
                # because this is a Horiontal container, the width
                # is always the gui width, but the HEIGHT is the max height
                i.build_image(width=-1, height=height)
            i.update_position(xpos, widget_ypos)
            image.blit(i.image, (xpos, widget_ypos))
            xpos += i.image.get_width() + (self.border * 2)
        return image

    def build_full_image(self, width, height):
        if height == -1:
            # use rect size
            width = self.minimum_size[1]
        image = Resources.colour_surface(width, height, self.background)
        # we fill the given space with the widgets.
        # what is our minimum size?
        sizes = [x.minimum_size for x in self.nodes]
        min_width = sum([x[0] for x in sizes])
        if min_width < width:
            # we have spare space, since we only worry about the vertical size
            # how do we distribute the space?
            if self.align_children == Align.LEFT:
                # everything to the left
                node_image = self.build_simple_image()
                # (0,0) -> no need to update positions
                image.blit(node_image, (0, 0))
                return image
        else:
            # must be same size
            return self.build_simple_image()
