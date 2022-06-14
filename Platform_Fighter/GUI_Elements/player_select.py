# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from Platform_Fighter.GUI_Elements import button
from Platform_Fighter.GUI_Elements import text
from Platform_Fighter.GUI_Elements.text import font

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)


# -------------------------------------------------------------------------
# Class Definitions
# -------------------------------------------------------------------------
class playerSelect(pygame.sprite.Sprite):
    def __init__(self, player, pos, color, display):
        super().__init__()
        self.font = font
        self.num_player = player
        self.playerText = text.Text("P%d" % self.num_player, self.font, 30, WHITE, (pos[0] + 100, pos[1] + 50), display)

        self.name = "Player %d" % self.num_player
        self.nameText = text.Text(self.name, self.font, 30, WHITE, (pos[0] + 100, pos[1] - 50), display)

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

            if self.skin is not None:
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
            else:
                if self.skin_position >= len(self.skins) - 1:
                    self.skin_position = 0
                else:
                    self.skin_position += 1
                self.skin = self.skins[self.skin_position]

        if character == "Square":
            self.characterSurf = pygame.Surface((100, 100))
            self.characterSurf.fill(self.skin)
            self.characterRect = self.characterSurf.get_rect(center=(self.pos[0] - 100, self.pos[1]))
            self.display.blit(self.characterSurf, self.characterRect)

        self.playerText.draw()
        self.nameText.draw()

    def get_pressed(self, click):
        # print(click)
        self.backButton.get_pressed(click)
        self.forwardButton.get_pressed(click)





