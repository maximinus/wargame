#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.gui_nodes import Label
from wargame.gui.window import Window


def game():
    controller = wargame.engine.init(os.getcwd())
    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # just display a button
    label = Label('Wargame Engine', (0, 0, 0), (214, 214, 214))
    window = Window(label)
    # add the window to a scene
    scene = Scene([background, window])
    controller.add_scene('start', scene)
    controller.run('start')


if __name__ == '__main__':
    game()
