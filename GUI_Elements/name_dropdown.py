import pygame
from pygame.locals import *
import time
import pandas as pd

font = 'impact'

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)


def text_objects(text, font, colour, center):
    textSurface = font.render(text, True, colour)
    textRect = textSurface.get_rect(center=center)
    return textSurface, textRect


def button(x, y, w, h, shape, display, rect=False):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1:
            # time.sleep(0.25)
            return True

    if not rect:
        pygame.draw.polygon(display, GRAY, shape)
    else:
        pygame.draw.rect(display, RED, (x, y, w, h), 1)
    pygame.draw.rect(display, RED, (x, y, w, h), 1)


class nameDrop:
    def __init__(self, pos, display):
        self.font = pygame.font.SysFont(font, 36)
        self.names = pd.read_csv("../Names/Names.csv").to_dict()
        if 'Unnamed: 0' in list(self.names.keys()):
            self.names.pop('Unnamed: 0')
        self.name = 'Player 1'
        self.controls = self.names[self.name]

        self.all_buttons = []
        self.all_texts = []
        self.key_lists = list(self.names.keys())
        self.key_lists.append("New Name")
        self.value_lists = list(self.names.values())
        for count, name in enumerate(self.key_lists):
            self.all_buttons.append(
                button(pos[0], pos[1] + (50 * (count + 1)), 200, 50 * len(self.names), (), display, True))
            self.all_texts.append(
                text_objects(name, self.font, WHITE, (pos[0] + 100, pos[1] + 25 + (50 * (count + 1)))))

        self.nameSurf, self.nameRect = text_objects(self.name, self.font, WHITE, (pos[0] + 100, pos[1]))
        self.pos = pos
        self.display = display
        self.pressed = False

    def update(self):
        if button(self.pos[0], self.pos[1] - 7, 30, 30,
                  ((self.pos[0], self.pos[1]), (self.pos[0] + 30, self.pos[1]), (self.pos[0] + 15, self.pos[1] + 15)),
                  self.display):
            self.pressed = True

        self.display.blit(self.nameSurf, self.nameRect)
        if self.pressed:
            pygame.draw.rect(self.display, BLACK, (self.pos[0], self.pos[1], 200, 50 * (len(self.names) + 1)))
            pygame.draw.rect(self.display, GRAY, (self.pos[0], self.pos[1], 200, 50 * (len(self.names) + 1)), 1)
            self.all_buttons = []

            for count, name in enumerate(self.key_lists):
                if button(self.pos[0], self.pos[1] + (50 * (count + 1)), 200, 50, (), self.display, True):
                    if name != "New Name":
                        self.name = name
                        self.controls = self.names[self.name]
                        self.nameSurf, self.nameRect = text_objects(self.name, self.font, WHITE,
                                                                    (self.pos[0] + 100, self.pos[1]))
                        self.pressed = False

                        return self.controls
                    else:
                        self.pressed = False

                self.display.blit(self.all_texts[count][0], self.all_texts[count][1])

        return None

    def saveControls(self, controls):
        temp = {0: controls[0], 1: controls[1], 2: controls[2], 3: controls[3], 4: controls[4]}
        self.names[self.name] = temp
        df = pd.DataFrame(self.names)
        df.to_csv("../Names/Names.csv")
