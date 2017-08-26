#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.nodes import VerticalContainer, Button
from wargame.gui.containers import Window
from wargame.message import Message
from wargame.events import MessageType


def game():
    resources = os.path.join(os.getcwd(), '../')
    controller = wargame.engine.init(resources)

    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')

    # a button needs 2 things - the text to display, and the message to send
    button = Button('Close', Message(MessageType.EXIT_GAME))
    bc = VerticalContainer([button], background=(214, 214, 214))
    window = Window(bc, xpos=-1, ypos=-1)

    # add the window to a scene
    scene = Scene([background, window])
    controller.add_scene('start', scene)
    controller.run('start')


if __name__ == '__main__':
    game()
