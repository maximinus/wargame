#!/usr/bin/env python

import os

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.tweens import FlashTween


# example of flashing Node2d


def game():
    # start the engine. It needs to know where the resources file is
    controller = wargame.engine.init(os.getcwd())
    # add a sprite. We need a position, and image
    sprite = ImageNode.from_image(100, 100, 'sprites.soldier')

    # we want the unit to flash every second, so add a tween
    # all times are in milliseconds for the engine
    sprite.tween = FlashTween(500)

    # I add the node to a new scene
    scene = Scene([sprite])
    # I add the scene to the engine
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
