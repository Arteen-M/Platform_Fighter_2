import pygame
import pandas as pd
from GUI_Elements import button

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


class nameDrop:
    def __init__(self, pos, display):
        self.font = pygame.font.SysFont(font, 36)
        self.names = pd.read_csv("../Names/Names.csv").to_dict()
        if 'Unnamed: 0' in list(self.names.keys()):
            self.names.pop('Unnamed: 0')
        self.name = 'Player 1'
        self.controls = self.names[self.name]

        self.all_texts = []
        self.key_lists = list(self.names.keys())
        self.key_lists.append("New Name")
        self.value_lists = list(self.names.values())
        for count, name in enumerate(self.key_lists):
            self.all_texts.append(text_objects(name, self.font, WHITE, (pos[0] + 100, pos[1] + 25 + (50 * (count + 1)))))

        self.nameSurf, self.nameRect = text_objects(self.name, self.font, WHITE, (pos[0] + 100, pos[1]))
        self.pos = pos
        self.display = display

        self.button = button.Button(self.pos[0], self.pos[1] - 7, 30, 30, ((self.pos[0], self.pos[1]), (self.pos[0] + 30, self.pos[1]), (self.pos[0] + 15, self.pos[1] + 15)), GRAY, RED, self.display, rect=False, draw=True, border=False)
        self.buttons_list = [button.Button(self.pos[0], self.pos[1] + (50 * (x + 1)), 200, 50, None, None, None, self.display, False, False, False) for x in range(len(self.key_lists))]

        self.pressed = False

    def update(self):
        self.button.update()
        self.display.blit(self.nameSurf, self.nameRect)

        if self.button.pressed or self.pressed:
            self.pressed = True
            pygame.draw.rect(self.display, BLACK, (self.pos[0], self.pos[1], 200, 50 * (len(self.names) + 1)))
            pygame.draw.rect(self.display, GRAY, (self.pos[0], self.pos[1], 200, 50 * (len(self.names) + 1)), 1)

            for count, name in enumerate(self.key_lists):
                self.buttons_list[count].update()
                if self.buttons_list[count].pressed:
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
