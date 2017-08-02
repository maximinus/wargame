#!/usr/bin/env python3

# implementation of queue messaging system

from collections import deque
import pygame

from wargame.message import Message
from wargame.events import MessageType


class MessageQueue:
    def __init__(self):
        self.queue = deque()
        self.listener = None

    def set_listener(self, listener):
        # call this scene to handle events
        self.listener = listener

    def add_message(self, message):
        # add this to the RIGHT of the queue
        self.queue.append(message)

    def add_priority_message(self, message):
        # priority? Add to the LEFT
        self.queue.appendleft(message)

    def handle(self):
        """
        Handle the next message
        Return True to quit pygame
        """
        # add all inputs as low priority
        # returns True if we quit the game
        if self.get_inputs():
            return True
        if self.empty:
            return False
        # take from the LEFT of the queue
        message = self.queue.popleft()

        # send to the scene
        if self.listener is not None:
            self.listener(message)
        return False

    def get_inputs(self):
        # add all input events to the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.add_message(Message(MessageType.EXIT_GAME, None))
            else:
                # timer or move?
                if event.type >= pygame.USEREVENT:
                    self.add_message(Message(event.type, None))
                else:
                    self.add_message(Message(event.type, event))
        return False

    def size(self):
        return len(self.queue)

    @property
    def empty(self):
        return len(self.queue) == 0


# singleton message system


MessageSystem = MessageQueue()
