#!/usr/bin/env python3

import os
import pygame

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.loader import Resources
from wargame.tweens import TweenResult

# example of moving Node2d


class MouseOverNode(ImageNode):
    def __init__(self, highlight, image, rect):
        super().__init__(rect, image)
        self.highlight = highlight
        self.normal_image = image
        self.messages.append(pygame.MOUSEMOTION)
        self.inside = False

    def handle(self, message):
        # this can only be a MOUSE_MOTION message
        # is the mouse in the rect?
        xpos = message.data.pos[0]
        ypos = message.data.pos[1]
        if self.rect.collidepoint(xpos, ypos):
            # mouse says inside
            if not self.inside:
                self.image = self.highlight
                self.tween_result = TweenResult(new=self.rect)
                self.inside = True
        else:
            if self.inside:
                self.image = self.normal_image
                self.tween_result = TweenResult(new=self.rect)
                self.inside = False

    def update(self, time_delta):
        pass


def game():
    controller = wargame.engine.init(os.getcwd())
    # we need 2 images to display mouse over and mouse not over
    red = Resources.colour_surface(200, 200, (255, 0, 0))
    blue = Resources.colour_surface(200, 200, (0, 0, 255))

    # we need a node
    node = MouseOverNode(blue, red, pygame.Rect(220, 140, 200, 200))

    # I add the node to a SCENE
    scene = Scene([node])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
