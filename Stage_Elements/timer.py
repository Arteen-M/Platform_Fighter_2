import pygame
import math
import time


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


class Timer:
    def __init__(self, timer, font, size, color, pos, display):
        # super().__init__()
        self.timer = timer
        self.start_time = time.time()
        self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.text = "%d:00" % self.timer
        self.textSurf = 0
        self.textRect = 0
        self.current_time = 0
        self.min = 0
        self.sec = 0
        self.pos = pos
        self.display = display
        self.time_out = False

    def update(self, current_time):
        self.current_time = current_time
        self.min = (self.timer * 60 - math.floor(self.current_time - self.start_time)) // 60
        self.sec = self.timer * 60 - math.floor(self.current_time - self.start_time) - self.min * 60

        if self.sec < 10:
            self.text = "%d:0%d" % (self.min, self.sec)
        else:
            self.text = "%d:%d" % (self.min, self.sec)

        self.textSurf, self.textRect = text_objects(self.text, self.font, self.color)
        self.textRect.center = self.pos

        self.display.blit(self.textSurf, self.textRect)

        if self.min == 0 and self.sec == 0:
            self.time_out = True
        else:
            self.time_out = False

