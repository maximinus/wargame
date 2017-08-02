#!/usr/bin/env python3

import logging
from box import Box
logger = logging.getLogger(__name__)


class BaseConfig:
    members = []
    name = 'BaseConfig'

    def __init__(self, data, path):
        # TODO: add member checking
        data['type'] = self.name
        self.data = Box(data)


class WindowBorderConfig(BaseConfig):
    members = ['image_rects', 'image', 'name', 'dimensions', 'background']
    name = 'WindowBorder'


CONFIGS = {'WindowBorder': WindowBorderConfig}


def get_config_item(data, path):
    if 'meta' not in data:
        logging.error('No meta in {0}'.format(path))
        return
    if 'type' not in data['meta']:
        logging.error('Error: No type in {0}'.format(path))
        return
    if data['meta']['type'] not in CONFIGS:
        logging.error('Unkown type {0} in {1}'.format(data['meta']['type'], path))
        return
    if 'data' not in data:
        logging.error('No data given in {0}'.format(path))
        return

    try:
        return CONFIGS[data['meta']['type']](data['data'], path)
    except ValueError:
        return
