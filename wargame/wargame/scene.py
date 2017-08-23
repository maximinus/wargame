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

    def get_tween_result(self):
        rects = []
        for node in self.nodes:
            if node.image is not None:
                rects.extend(node.tween_result)
        return rects

    def process_tweens(self):
        time_now = time.perf_counter()
        time_delta = time_now - self.last_tick
        self.last_tick = time_now
        # calculate millisecoonds since last update
        time_delta = int(time_delta * 1000)
        for node in self.nodes:
            node.update(time_delta)

    def draw_dirty_background(self, tween):
        if tween.old is not None:
            self.screen.blit(self.background, tween.old, tween.old)
        if tween.new is not None:
            self.screen.blit(self.background, tween.new, tween.new)

    def update_screen(self):
        self.process_tweens()
        # go through displayable nodes
        nodes = [x for x in self.nodes if x.displayable]
        display_nodes = [x for x in nodes if x.tween_result is not None]
        for node in display_nodes:
            self.draw_dirty_background(node.tween_result)
        # check if they have some dirty rects
        for node in display_nodes:
            node.draw_dirty(node, node.tween_result, self.screen)
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
