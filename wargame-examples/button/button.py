#!/usr/bin/env python3

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.loader import Resources
from wargame.gui.gui_nodes import HorizontalContainer, VerticalContainer, GuiImage
from wargame.gui.window import Window, Button


def game():
    controller = wargame.engine.init(os.getcwd())
    # let's have a background
    background = ImageNode.from_image(0, 0, 'sprites.wallpaper')

    # start by getting 3 buttons
    button1 = Button('Wargame')
    button2 = Button('Engine')
    button3 = Button('By Chris')
    container1 = HorizontalContainer([button1, button2, button3], background=(214, 214, 214))
    # and a logo
    logo = GuiImage.from_image('sprites.logo')
    container2 = VerticalContainer([logo, container1], background=(214, 214, 214))
    window = Window(container2)

    # add the window to a scene
    scene = Scene([background, window])
    controller.add_scene('start', scene)
    controller.run('start')


if __name__ == '__main__':
    game()
