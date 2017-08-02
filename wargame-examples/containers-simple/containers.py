#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.gui.gui_nodes import VerticalContainer
from wargame.gui.window import Window
from wargame.nodes import ImageNode


def game():
    controller = wargame.engine.init(os.getcwd())
    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # we want a window to display with a VerticalContainer
    node1 = ImageNode.from_image(0, 0, 'sprites.dog')
    node2 = ImageNode.from_image(0, 0, 'sprites.pattern')
    container = VerticalContainer([node2, node1, node2], (214, 214, 214))
    window = Window(container)
    # add the window to a scene
    scene = Scene([background, window])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
