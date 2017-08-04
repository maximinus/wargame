#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.gui_nodes import GuiNode, HorizontalContainer, VerticalContainer
from wargame.gui.layout import Align
from wargame.gui.window import Window
from wargame.loader import Resources


def game():
    controller = wargame.engine.init(os.getcwd())
    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # we want a window to display with a HorizontalContainer
    node1 = GuiNode.from_image(Resources.colour_surface(100, 100, (200, 32, 32)))
    node2 = GuiNode.from_image(Resources.colour_surface(100, 50, (32, 200, 32)))
    node3 = GuiNode.from_image(Resources.colour_surface(100, 50, (32, 32, 200)))
    container1 = VerticalContainer([node1, node2, node3], (214, 214, 214), align=Align.TOP)

    node6 = GuiNode.from_image(Resources.colour_surface(100, 50, (32, 32, 200)))
    node5 = GuiNode.from_image(Resources.colour_surface(100, 50, (32, 200, 32)))
    node4 = GuiNode.from_image(Resources.colour_surface(100, 100, (200, 32, 32)))
    container2 = VerticalContainer([node6, node5, node4], (214, 214, 214), align=Align.TOP)

    hcontainer = HorizontalContainer([container1, container2], (214, 214, 214), align=Align.CENTRE)
    window = Window(hcontainer)

    # add the window to a scene
    scene = Scene([background, window])
    controller.add_scene('start', scene)
    controller.run('start')


if __name__ == '__main__':
    game()
