import pygame
import time
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


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

"""
def button(x, y, w, h, shape, display):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1:
            time.sleep(0.25)
            return True

    pygame.draw.polygon(display, GRAY, shape)
    # pygame.draw.rect(display, RED, (x, y, w, h), 1)
"""


class playerSelect(pygame.sprite.Sprite):
    def __init__(self, player, pos, color, display):
        super().__init__()
        self.font = pygame.font.SysFont(font, 30)
        self.num_player = player
        self.playerSurf, self.playerRect = text_objects("P%d" % self.num_player, self.font, WHITE)
        self.playerRect.center = (pos[0] + 100, pos[1] + 50)

        self.name = "Player %d" % self.num_player
        self.nameSurf, self.nameRect = text_objects(self.name, self.font, WHITE)
        self.nameRect.center = (pos[0] + 100, pos[1] - 50)

        self.surf = pygame.Surface((350, 200))
        self.pos = pos
        self.rect = self.surf.get_rect(center=self.pos)

        self.color = color

        self.characterSurf = None
        self.characterRect = None

        self.skins = None
        self.skin = None
        self.skin_position = 0

        self.backButton = button.Button(self.pos[0] - 170, self.pos[1] + 58, 30, 35, ((self.pos[0] - 150, self.pos[1] + 60), (self.pos[0] - 150, self.pos[1] + 90), (self.pos[0] - 165, self.pos[1] + 75)), GRAY, None, display, draw=True)
        self.forwardButton = button.Button(self.pos[0] - 70, self.pos[1] + 58, 30, 35, ((self.pos[0] - 50, self.pos[1] + 60), (self.pos[0] - 50, self.pos[1] + 90), (self.pos[0] - 35, self.pos[1] + 75)), GRAY, None, display, draw=True)
        # self.characterSurf = pygame.Surface((100, 100))
        # self.characterSurf.fill(self.color)
        # self.characterRect = self.characterSurf.get_rect(center=self.pos)

        self.display = display

    def update(self, character, skins):
        pygame.draw.rect(self.display, self.color, self.rect, 1)
        self.forwardButton.update()
        self.backButton.update()

        if skins is not None:
            self.skins = skins
            self.skin = self.skins[self.skin_position]

            if self.backButton.pressed:
                if self.skin_position == 0:
                    self.skin_position = len(self.skins) - 1
                else:
                    self.skin_position -= 1
                self.backButton.pressed = False

            if self.forwardButton.pressed:
                if self.skin_position == len(self.skins) - 1:
                    self.skin_position = 0
                else:
                    self.skin_position += 1

                self.forwardButton.pressed = False

        if character == "Square":
            self.characterSurf = pygame.Surface((100, 100))
            self.characterSurf.fill(self.skin)
            self.characterRect = self.characterSurf.get_rect(center=(self.pos[0] - 100, self.pos[1]))
            self.display.blit(self.characterSurf, self.characterRect)

        self.display.blit(self.playerSurf, self.playerRect)
        self.display.blit(self.nameSurf, self.nameRect)

    def get_pressed(self, click):
        # print(click)
        self.backButton.get_pressed(click)
        self.forwardButton.get_pressed(click)





