#!/usr/bin/env python

import os
import pygame

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.tweens import MoveTween


# example of moving Node2d


def game():
    controller = wargame.engine.init(os.getcwd())
    # add a sprite from an image
    sprite = ImageNode.from_image(100, 100, 'sprites.soldier')

    # we want the unit to move, so add a tween
    # all times are in milliseconds for the engine
    # this move rect is a VECTOR, so we move by this amount
    move = pygame.Rect(300, 0, 0, 0)
    sprite.tween = MoveTween(4000, sprite.rect, move)

    # I add the node to a SCENE
    scene = Scene([sprite])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
