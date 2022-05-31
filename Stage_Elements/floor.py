import pygame
from pygame.locals import *
import sys

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)


class Floor(pygame.sprite.Sprite):
    def __init__(self, display, dimensions=(100, 20), pos=(WIDTH/2, HEIGHT/2), color=BLUE):
        super().__init__()
        self.surf = pygame.Surface(dimensions)
        self.rect = self.surf.get_rect(center=pos)

        self.color = color
        self.surf.fill(self.color)

        self.display = display

    def draw(self):
        self.display.blit(self.surf, self.rect)




