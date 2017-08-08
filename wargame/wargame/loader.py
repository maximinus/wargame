#!/usr/bin/env python3

import os
import pygame
import yaml
from pathlib import PurePath
from logzero import logger

from wargame.configs.gfx import get_config_item


class ConfigLoader:
    """
    Load and return the config files
    """
    def __init__(self):
        self.data = {}

    def load(self, root_folder):
        # config files under ROOT/resources/config
        # iterate through those files
        for subdir, dirs, files in os.walk(root_folder):
            for file in files:
                # load this yaml file
                filepath = os.path.join(subdir, file)
                data = yaml.load(open(filepath, 'r'))
                path = PurePath(filepath).parts
                path = '/'.join(path[path.index('resources'):])
                config = get_config_item(data, path)
                if config is None:
                    logger.error('Failed to load {0}'.format(path))
                    continue
                # store this item
                self.data[config.data.type] = config.data

    def get(self, data_type):
        return self.data[data_type]


class ResourceHandler:
    def __init__(self):
        """
        At this point, pygame window is not setup
        Do not doing any image creation or loading
        """
        self.images = {}
        self.fonts = {}
        self.path = '.'
        self.error_image = None
        self.configs = None

    def load_resources(self, resources, screen):
        self.screen = screen
        self.build_error_image()
        if resources is None:
            return
        self.path = os.path.join(resources, 'resources')
        self.load_images(os.path.join(self.path, 'gfx'))
        self.configs = ConfigLoader()
        self.configs.load(os.path.join(self.path, 'config'))
        self.load_fonts(os.path.join(self.path, 'fonts'))

    def load_images(self, gfx_folder):
        for folder in ['hexes', 'sprites', 'gui']:
            # if the folder exists, load from it
            path = os.path.join(gfx_folder, folder)
            if os.path.exists(path):
                self.load_image_folder(path, folder)

    def load_fonts(self, font_folder):
        font_config = self.configs.get('Fonts')
        for i in font_config.fonts:
            filepath = os.path.join(font_folder, font_config.fonts[i].file)
            size = font_config.fonts[i].size
            try:
                self.fonts[i] = pygame.font.Font(filepath, size)
            except OSError:
                logger.error('Could not load font {0}'.format(filepath))
        # store a standard font
        self.fonts['default'] = self.fonts[font_config.default]

    def load_image_folder(self, folder, namespace):
        # loop through files in given folder
        for filename in os.listdir(folder):
            name = filename.split('.')[0]
            path = os.path.join(folder, filename)
            try:
                image = pygame.image.load(path).convert_alpha()
                self.images['{0}.{1}'.format(namespace, name)] = image
            except pygame.error:
                logger.error('Could not load image {0}'.format(path))

    def build_error_image(self):
        """
        The image to return if we cannot find what was asked for
        """
        self.error_image = pygame.Surface((32, 32)).convert()
        # flood fill with red
        self.error_image.fill((255, 0, 0))

    def get_image(self, image_name):
        try:
            return self.images[image_name]
        except KeyError:
            logger.error('No image name {0}'.format(image_name))
            return self.error_image

    def get_font(self, name='default'):
        try:
            font = self.fonts[name]
        except KeyError:
            logger.warn('Asked for missing font {0} in resources'.format(name))
            font = self.fonts['default']
        return font

    def colour_surface(self, width, height, colour):
        surface = pygame.Surface((width, height)).convert()
        surface.fill(colour)
        return surface

    def get_centre(self, width, height):
        # given width and height of a rect, return thr (xpos, ypos)
        # that would display this in the centre
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        centre_x = (screen_width - width) // 2
        centre_y = (screen_height - height) // 2
        return [centre_x, centre_y]


Resources = ResourceHandler()
