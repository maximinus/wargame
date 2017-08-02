#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.gui.window import Window
from wargame.nodes import ImageNode


def game():
    controller = wargame.engine.init(os.getcwd())
    # let's have a background for a change.
    # a very simple ImageNode will do
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # this time, we want a window to display
    # but a window must display 'something', so we'll use an ImageNode
    window_contents = ImageNode.from_image(0, 0, 'sprites.dog')
    window = Window(window_contents)
    # add the window to a scene
    scene = Scene([background, window])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
