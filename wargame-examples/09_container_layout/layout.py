#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.nodes import GuiImage, VerticalContainer
from wargame.gui.layout import Align
from wargame.gui.containers import Window
from wargame.loader import Resources


def game():
    resources = os.path.join(os.getcwd(), '../')
    controller = wargame.engine.init(resources)

    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # we want a window to display with a VerticalContainer
    node1 = GuiImage(Resources.colour_surface(200, 80, (200, 32, 32)))
    node2 = GuiImage(Resources.colour_surface(175, 80, (32, 200, 32)), align=Align.CENTRE_RIGHT)
    node3 = GuiImage(Resources.colour_surface(150, 80, (32, 32, 200)))
    container = VerticalContainer([node1, node2, node3], (214, 214, 214), align_children=Align.CENTRE_LEFT)
    window = Window(container)
    # add the window to a scene
    scene = Scene([background, window])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
