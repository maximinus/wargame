#!/usr/bin/env python3

import time
import pygame

from wargame.loader import Resources
from wargame.events import MessageType

import logging
logger = logging.getLogger(__name__)

# a scene blocks all other gfx, music and input.
# scenes do not know about images, since the nodes do that


class Scene:
    def __init__(self, nodes):
        self.nodes = nodes
        self.screen = Resources.screen
        self.last_tick = 0
        size = (self.screen.get_width(), self.screen.get_height())
        self.background = pygame.Surface(size).convert()
        self.background.fill((0, 0, 0))

    def add_node(self, node):
        self.nodes.append(node)

    def process_tweens(self):
        time_now = time.perf_counter()
        time_delta = time_now - self.last_tick
        self.last_tick = time_now
        # calculate millisecoonds since last update
        time_delta = int(time_delta * 1000)
        dirty_rects = []
        for node in self.nodes:
            dirty_rects.extend(node.update(time_delta))
        return dirty_rects

    def draw_dirty_background(self, rect):
        self.screen.blit(self.background, rect, rect)

    def update_screen(self):
        dirty_rects = self.process_tweens()
        # only refresh displayable nodes
        nodes = [x for x in self.nodes if x.displayable]
        # draw the dirty background
        for rect in dirty_rects:
            self.draw_dirty_background(rect)
        # loop through all dirty rects
        for rect in dirty_rects:
            # then loop through all display nodes
            for node in nodes:
                node.draw_dirty(rect, self.screen)
        pygame.display.flip()

    def draw(self):
        # set our timer
        self.last_tick = time.perf_counter()
        # clean draw of the scene
        for node in [x for x in self.nodes if x.displayable]:
            if node.visible:
                self.screen.blit(node.image, node.rect)

    def handle(self, message):
        # maybe I want it?
        if message.message_id == MessageType.UPDATE_SCREEN:
            return self.update_screen()
        for node in self.nodes:
            # let the node decide what it has to
            if node.handle(message):
                return
