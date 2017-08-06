#!/usr/bin/env python3

import os
import sys
import logging
import pygame

from wargame.loader import Resources
from wargame.scheduler import MessageSystem
from wargame.events import MessageType
logger = logging.getLogger(__name__)


class HexGameController:
    def __init__(self, resource_directory):
        self.screen = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
        pygame.display.set_caption('HexGame')
        Resources.load_resources(resource_directory, self.screen)
        self.clock = pygame.time.Clock()
        self.scenes = {}
        self.current_scene = None
        self.last_tick = 0
        self.setup_logging(resource_directory)

    def setup_logging(self, resource_directory):
        log_file = os.path.join(resource_directory, 'resources', 'wargame.log')
        logging.basicConfig(filename=log_file, level=logging.DEBUG)

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def run(self, scene_name):
        try:
            self.current_scene = self.scenes[scene_name]
        except KeyError:
            logging.error('Error: No such scene "{0}"'.format(scene_name))
            return False
        self.current_scene.draw()
        pygame.display.flip()
        # add a timer for gfx events. Update the screen every x milliseconds
        # 30 FPS = 1000 / 30 = ~33. 20 FPS = 1000 / 20 = 50
        pygame.time.set_timer(MessageType.UPDATE_SCREEN, 50)
        # run the game loop
        MessageSystem.set_listener(self.handle)
        while not MessageSystem.handle():
            pass

    def handle(self, message):
        # exit?
        if message.message_id == MessageType.EXIT_GAME:
            logging.info('Exiting')
            sys.exit(True)
        # send message to scene if required
        return self.current_scene.handle(message)


def init(resource_directory=None):
    logging.info('Starting')
    pygame.init()
    # do system checks
    if not pygame.font:
        logging.error('Error: Fonts disabled')
        return False
    if not pygame.mixer:
        logging.error('Error: Sound disabled')
        return False

    controller = HexGameController(resource_directory)
    return controller
