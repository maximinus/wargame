#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.containers import Window
from wargame.gui.nodes import GuiImage


def game():
    resources = os.path.join(os.getcwd(), '../')
    controller = wargame.engine.init(resources)

    # let's have a background for a change.
    # a very simple ImageNode will do
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # this time, we want a window to display
    # but a window must display 'something', so we'll use an ImageNode
    window_contents = GuiImage.from_image('sprites.dog')
    window = Window(window_contents)
    # add the window to a scene
    scene = Scene([background, window])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
