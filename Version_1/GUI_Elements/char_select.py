import pygame
from Version_1.GUI_Elements import button
from Version_1.GUI_Elements import text
from Version_1.GUI_Elements.text import font

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


class charButton(pygame.sprite.Sprite):
    def __init__(self, pos, name, display, color, image=None):
        super().__init__()
        self.surf = pygame.Surface((75 * 2, 75 * 2))
        self.pos = pos
        self.rect = self.surf.get_rect(center=self.pos)
        self.name = name
        self.font = font

        self.text = text.Text(self.name, self.font, 30, WHITE, (self.pos[0], self.pos[1] - 60), display)

        self.display = display

        self.color = color

        if image is None:
            self.image = pygame.Surface((85, 85))
            self.image.fill(self.color)
        else:
            self.image = image

        self.image_rect = self.image.get_rect(center=(self.pos[0], self.pos[1] + 15))

        self.button = button.Button(self.rect.x, self.rect.y, self.rect.w, self.rect.h, (), WHITE, WHITE, self.display, rect=True, draw=False, border=True)

    def update(self):
        self.button.update()
        self.text.draw()
        self.display.blit(self.image, self.image_rect)

    def get_pressed(self, click):
        self.button.get_pressed(click)
