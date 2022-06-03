import pygame
import math


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


class Graphic:
    def __init__(self, display, font, size, pos, color):
        self.text = "0%"
        self.font = pygame.font.SysFont(font, size)
        self.pos = pos
        self.textSurf = 0
        self.textRect = 0
        self.color = color
        self.display = display

    def update(self, percentage):
        self.text = str(math.floor(percentage)) + "%"
        self.textSurf, self.textRect = text_objects(self.text, self.font, self.color)
        self.textRect.center = self.pos

        self.display.blit(self.textSurf, self.textRect)


