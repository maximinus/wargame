#!/usr/bin/env python3

import pygame


class MessageIndex:
    def __init__(self):
        self.index = pygame.USEREVENT
        self.pool = []

    def get_index(self):
        self.index += 1
        return self.index

    def get_new(self):
        if self.pool:
            return self.pool.pop()
        return self.get_index()

    def release(self, message_id):
        self.pool.append(message_id)


DEFAULTS = ['EXIT_GAME']

MessageType = MessageIndex()

# standard update screen event
setattr(MessageType, 'UPDATE_SCREEN', pygame.USEREVENT)
for x in DEFAULTS:
    setattr(MessageType, x, MessageType.get_index())
