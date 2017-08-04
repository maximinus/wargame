#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.gui_nodes import GuiNode, VerticalContainer
from wargame.gui.layout import Align
from wargame.gui.window import Window
from wargame.loader import Resources


def game():
    controller = wargame.engine.init(os.getcwd())
    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # we want a window to display with a VerticalContainer
    node1 = GuiNode.from_image(Resources.colour_surface(200, 80, (200, 32, 32)))
    node2 = GuiNode.from_image(Resources.colour_surface(175, 80, (32, 200, 32)), align=Align.CENTRE_RIGHT)
    node3 = GuiNode.from_image(Resources.colour_surface(150, 80, (32, 32, 200)))
    container = VerticalContainer([node1, node2, node3], (214, 214, 214), align=Align.CENTRE_LEFT)
    window = Window(container)
    # add the window to a scene
    scene = Scene([background, window])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
