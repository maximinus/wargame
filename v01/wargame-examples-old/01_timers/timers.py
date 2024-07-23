#!/usr/bin/env python

import os

import wargame_old.engine
from wargame_old.scene import Scene
from wargame_old.nodes import RegularEvent


def handle(message):
    print('Hello, World')


def game():
    resources = os.path.join(os.getcwd(), '../')
    controller = wargame_old.engine.init(resources)
    # we will add a RegularEvent object to the scene
    # this will just send a timer message to itself
    timer = RegularEvent(2000, handle)
    # I add the node to a SCENE
    scene = Scene([timer])
    # I add the scene to the ENGINE
    controller.add_scene('start', scene)
    # I tell the engine what scene to start and run the controller
    controller.run('start')


if __name__ == '__main__':
    game()
