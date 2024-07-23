import sys
import pygame
from pygame import Vector2

DEFAULT_SIZE = Vector2(800, 600)
CLOCK_FPS = 60


def await_keypress():
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            return


class Engine:
    def __init__(self, scene, size=None, title='Wargame'):
        if size is None:
            size = DEFAULT_SIZE
        pygame.init()
        self.display = pygame.display.set_mode((size.x, size.y))
        pygame.display.set_caption(title)
        self.scene = scene
        self.screen_size = size
        self.centre_offset = Vector2(size.x // 2, size.y // 2)

    def loop(self):
        # render the scene and wait for a keypress
        self.display.fill((255, 255, 255))
        self.scene.render()
        self.display.blit(self.scene.surface, (0, 0))
        pygame.display.flip()
        await_keypress()
