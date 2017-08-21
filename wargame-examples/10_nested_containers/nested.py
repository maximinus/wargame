#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.gui.nodes import GuiImage, HorizontalContainer, VerticalContainer
from wargame.gui.layout import Align
from wargame.gui.containers import Window
from wargame.loader import Resources


def game():
    resources = os.path.join(os.getcwd(), '../')
    controller = wargame.engine.init(resources)

    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')
    # we want a window to display with a HorizontalContainer
    node1 = GuiImage(Resources.colour_surface(100, 30, (200, 32, 32)))
    node2 = GuiImage(Resources.colour_surface(100, 30, (32, 200, 32)))
    node3 = GuiImage(Resources.colour_surface(100, 30, (32, 32, 200)))
    c1 = VerticalContainer([node1, node2, node3], (214, 214, 214), align_children=Align.TOP)

    node6 = GuiImage(Resources.colour_surface(100, 50, (32, 32, 200)))
    node5 = GuiImage(Resources.colour_surface(100, 50, (32, 200, 32)))
    node4 = GuiImage(Resources.colour_surface(100, 100, (200, 32, 32)))
    c2 = VerticalContainer([node6, node5, node4], (214, 214, 214), align_children=Align.TOP)

    node7 = GuiImage(Resources.colour_surface(100, 30, (200, 32, 32)))
    node8 = GuiImage(Resources.colour_surface(100, 30, (32, 200, 32)))
    node9 = GuiImage(Resources.colour_surface(100, 30, (32, 32, 200)))
    c3 = VerticalContainer([node7, node8, node9], (214, 214, 214), align_children=Align.TOP)

    hcontainer = HorizontalContainer([c1, c2, c3], (214, 214, 214), align_children=Align.TOP)
    window = Window(hcontainer)

    # add the window to a scene
    scene = Scene([background, window])
    controller.add_scene('start', scene)
    controller.run('start')


if __name__ == '__main__':
    game()
