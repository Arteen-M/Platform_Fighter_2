import pygame
import math


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


class Graphic:
    def __init__(self, display, font, size, pos, color, side=True, stocks=3, img=None):
        self.text = "0%"
        self.font = pygame.font.SysFont(font, size)
        self.pos = pos
        self.textSurf = 0
        self.textRect = 0
        self.color = color
        self.display = display
        self.total_stocks = stocks
        self.stocks = 0
        if side:
            self.side = -70
        else:
            self.side = 40
        self.image = img

    def update(self, percentage, stocks):
        self.stocks = stocks
        self.text = str(math.floor(percentage)) + "%"

        self.textSurf, self.textRect = text_objects(self.text, self.font, self.color)
        self.textRect.center = self.pos

        self.display.blit(self.textSurf, self.textRect)
        if self.image is None:
            """
            if self.stocks == 1:
                pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side, self.pos[1] - 15, 30, 30))
            if self.stocks == 2:
                pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side, self.pos[1] - 35, 30, 30))
                pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side, self.pos[1] + 5, 30, 30))
            if self.stocks == 3:
                pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side, self.pos[1] - 55, 30, 30))
                pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side, self.pos[1] - 15, 30, 30))
                pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side, self.pos[1] + 25, 30, 30))
            """
            for num in range(self.stocks):
                pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side, self.pos[1] - 55 + (40 * num), 30, 30))



