#!/usr/bin/env python3

import os
import sys
import pygame
import logzero
from logzero import logger

from wargame.loader import Resources
from wargame.scheduler import MessageSystem
from wargame.events import MessageType
from wargame.constants import VERSION


class HexGameController:
    def __init__(self, resource_directory):
        self.setup_logging(resource_directory)
        logger.info('Starting Wargame v{0}'.format(VERSION))
        system_checks()
        self.screen = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
        pygame.display.set_caption('HexGame')
        Resources.load_resources(resource_directory, self.screen)
        self.clock = pygame.time.Clock()
        self.scenes = {}
        self.current_scene = None
        self.last_tick = 0

    def setup_logging(self, resource_directory):
        log_file = os.path.join(resource_directory, 'resources', 'wargame.log')
        logzero.logfile(log_file)

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def run(self, scene_name):
        try:
            self.current_scene = self.scenes[scene_name]
        except KeyError:
            logger.error('Error: No such scene "{0}"'.format(scene_name))
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
            logger.info('Exiting Wargame')
            sys.exit(True)
        # send message to scene if required
        return self.current_scene.handle(message)


def system_checks():
    # do system checks
    if not pygame.font:
        logger.error('Error: Fonts disabled')
        sys.exit(False)
    if not pygame.mixer:
        logger.error('Error: Sound disabled')
        sys.exit(False)


def init(resource_directory=None):
    pygame.init()
    controller = HexGameController(resource_directory)
    return controller
