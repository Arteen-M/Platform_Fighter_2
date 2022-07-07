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


# -------------------------------------------------------------------------
# Class Definition
# -------------------------------------------------------------------------
class charButton(pygame.sprite.Sprite):
    def __init__(self, pos, name, display, color, image=None, scale=None):
        super().__init__()
        self.surf = pygame.Surface((75 * 2, 75 * 2))
        self.pos = pos
        self.rect = self.surf.get_rect(center=self.pos)
        self.name = name
        self.font = font

        # Text for character name
        self.text = text.Text(self.name, self.font, 30, WHITE, (self.pos[0], self.pos[1] - 60), display)

        self.display = display

        self.color = color

        if image is None:
            self.image = pygame.Surface((85, 85))
            self.image.fill(self.color)
        else:
            self.image = pygame.image.load(image).convert_alpha()

        if scale is not None:
            self.image = pygame.transform.scale(self.image, scale)

        self.image_rect = self.image.get_rect(center=(self.pos[0], self.pos[1] + 15))

        # Button for selecting
        self.button = button.Button(self.rect.x, self.rect.y, self.rect.w, self.rect.h, (), WHITE, WHITE, self.display, rect=True, draw=False, border=True)

    def update(self):
        # Draw everything
        self.button.update()
        self.text.draw()
        self.display.blit(self.image, self.image_rect)

    def get_pressed(self, click):
        # Set the button state
        self.button.get_pressed(click)
