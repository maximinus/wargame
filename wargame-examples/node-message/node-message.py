#!/usr/bin/env python3

import os
import pygame

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.loader import Resources
from wargame.tweens import TweenResult
from wargame.scheduler import MessageSystem
from wargame.message import Message
from wargame.events import MessageType

# example of moving Node2d


class NodeTransmit(ImageNode):
    def __init__(self, highlight, image, rect):
        super().__init__(rect, image)
        self.highlight = highlight
        self.normal_image = image
        self.messages.append(pygame.MOUSEMOTION)
        self.inside = False
        # create a new message type and save it
        self.message_id = MessageType.get_new()

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
                MessageSystem.add_message(Message(self.message_id, True))
        else:
            if self.inside:
                self.image = self.normal_image
                self.tween_result = TweenResult(new=self.rect)
                self.inside = False
                MessageSystem.add_message(Message(self.message_id, False))

    def update(self, time_delta):
        pass


class NodeReceive(ImageNode):
    def __init__(self, highlight, image, rect, message_id):
        super().__init__(rect, image)
        self.messages.append(message_id)
        self.normal = image
        self.highlight = highlight

    def handle(self, message):
        if message.data:
            # inside
            self.image = self.highlight
        else:
            self.image = self.normal
        self.tween_result = TweenResult(new=self.rect)

    def update(self, time_delta):
        pass


def game():
    controller = wargame.engine.init(os.getcwd())

    # this time, we want 1 node to control 2 other nodes

    # we need 2 images to display mouse over and mouse not over
    red = Resources.colour_surface(128, 128, (255, 0, 0))
    blue = Resources.colour_surface(128, 128, (0, 0, 255))
    green = Resources.colour_surface(128, 128, (0, 255, 0))

    # we need a node
    sender = NodeTransmit(green, blue, pygame.Rect(256, 173, 128, 128))
    receive1 = NodeReceive(blue, red, pygame.Rect(64, 176, 128, 128), sender.message_id)
    receive2 = NodeReceive(blue, red, pygame.Rect(448, 176, 128, 128), sender.message_id)

    # add the nodes to a SCENE
    scene = Scene([sender, receive1, receive2])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
