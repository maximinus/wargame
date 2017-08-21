#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.nodes import GuiImage, VerticalContainer
from wargame.gui.containers import Window


def game():
    resources = os.path.join(os.getcwd(), '../')
    controller = wargame.engine.init(resources)

    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # we want a window to display with a VerticalContainer
    node1 = GuiImage.from_image('sprites.dog')
    node2 = GuiImage.from_image('sprites.pattern')
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
