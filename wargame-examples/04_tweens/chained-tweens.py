#!/usr/bin/env python

import os
import pygame

import wargame.engine
from wargame.scene import Scene
from wargame.nodes import ImageNode
from wargame.tweens import ChainedTween, MoveTween


# example of moving Node2d


def game():
    resources = os.path.join(os.getcwd(), '../')
    controller = wargame.engine.init(resources)
    # add a sprite from an image
    sprite = ImageNode.from_image(100, 100, 'sprites.soldier')

    # add a chained tween with >1 tween
    sprite.tween = ChainedTween([MoveTween(500, sprite.rect, pygame.Rect(100, 0, 0, 0)),
                                 MoveTween(500, sprite.rect, pygame.Rect(0, 100, 0, 0)),
                                 MoveTween(500, sprite.rect, pygame.Rect(-100, 0, 0, 0)),
                                 MoveTween(500, sprite.rect, pygame.Rect(0, -100, 0, 0))], loop=True)

    # I add the node to a SCENE
    scene = Scene([sprite])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
