#!/usr/bin/env python3

# messages for queues


class Message:
    def __init__(self, message_id, data):
        self.message_id = message_id
        self.data = data

    def __repr__(self):
        return '{0}:{1}'.format(self.message_id, self.data)
