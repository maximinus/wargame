#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.gui_nodes import GuiNode
from wargame.gui.window import Button, Window
from wargame.loader import Resources


def game():
    controller = wargame.engine.init(os.getcwd())
    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # just display a button
    node = GuiNode.from_image(Resources.colour_surface(100, 30, (200, 32, 32)))
    button = Button(node)
    window = Window(button)
    # add the window to a scene
    scene = Scene([background, window])
    controller.add_scene('start', scene)
    controller.run('start')


if __name__ == '__main__':
    game()
