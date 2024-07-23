#!/usr/bin/env python3

import os

import wargame_old.engine
from wargame_old.scene import Scene
from wargame_old.nodes import ImageNode
from wargame_old.gui.nodes import VerticalContainer, Button
from wargame_old.gui.containers import Window
from wargame_old.message import Message
from wargame_old.events import MessageType


def game():
    resources = os.path.join(os.getcwd(), '../')
    controller = wargame_old.engine.init(resources)

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
