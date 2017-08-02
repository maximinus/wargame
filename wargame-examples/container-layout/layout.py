#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.gui.gui_nodes import VerticalContainer
from wargame.gui.layout import Align
from wargame.gui.window import Window
from wargame.nodes import ImageNode


def game():
    controller = wargame.engine.init(os.getcwd())
    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # we want a window to display with a VerticalContainer
    node1 = ImageNode.from_colour(200, 80, (200, 32, 32))
    node2 = ImageNode.from_colour(175, 80, (32, 200, 32))
    node3 = ImageNode.from_colour(150, 80, (32, 32, 200))
    container = VerticalContainer([node1, node2, node3], (214, 214, 214), align=Align.LEFT)
    window = Window(container)
    # add the window to a scene
    scene = Scene([background, window])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
