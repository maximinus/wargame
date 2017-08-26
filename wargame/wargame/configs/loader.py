#!/usr/bin/env python3

import logging
from box import Box
logger = logging.getLogger(__name__)

from wargame.configs.window import WindowLoader


class BaseConfig:
    members = []
    name = 'BaseConfig'

    def __init__(self, data):
        # TODO: add member checking
        data['type'] = self.name
        self.data = Box(data)


class WindowBorderConfig(BaseConfig):
    members = ['image_rects', 'image', 'name', 'dimensions', 'background']
    name = 'WindowBorder'


class ButtonConfig(BaseConfig):
    members = ['image_rects', 'image', 'name', 'dimensions', 'background']
    name = 'ButtonBorder'


class FontConfig(BaseConfig):
    members = ['fonts', 'default']
    name = 'Fonts'


class WindowConfig(BaseConfig):
    members = ['position', 'nodes']
    name = 'Window'


CONFIGS = {'WindowBorder': WindowBorderConfig,
           'ButtonBorder': ButtonConfig,
           'Fonts': FontConfig,
           'WindowConfig': WindowConfig}


def get_config_item(data, path):
    if 'meta' not in data:
        logging.error('No meta in {0}'.format(path))
        return
    if 'type' not in data['meta']:
        logging.error('Error: No type in {0}'.format(path))
        return
    if data['meta']['type'] not in CONFIGS:
        logging.error('Unknown type {0} in {1}'.format(data['meta']['type'], path))
        return
    if 'data' not in data:
        logging.error('No data given in {0}'.format(path))
        return

    try:
        config = CONFIGS[data['meta']['type']](data['data'])
        return config
    except ValueError:
        return
