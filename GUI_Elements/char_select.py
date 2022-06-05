import pygame

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


def button(x, y, w, h, display):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1:
            return True

    pygame.draw.rect(display, WHITE, (x, y, w, h), 1)


class charButton(pygame.sprite.Sprite):
    def __init__(self, pos, name, display, color, image=None):
        super().__init__()
        self.surf = pygame.Surface((75 * 2, 75 * 2))
        self.pos = pos
        self.rect = self.surf.get_rect(center=self.pos)
        self.name = name
        self.font = pygame.font.SysFont(font, 30)

        self.textSurf, self.textRect = text_objects(self.name, self.font, WHITE)
        self.textRect.center = (self.pos[0], self.pos[1] - 60)

        self.display = display

        self.color = color

        if image is None:
            self.image = pygame.Surface((85, 85))
            self.image.fill(self.color)
        else:
            self.image = image

        self.image_rect = self.image.get_rect(center=(self.pos[0], self.pos[1] + 15))

        self.button = False

    def update(self):
        self.button = button(self.rect.x, self.rect.y, self.rect.w, self.rect.h, self.display)
        self.display.blit(self.textSurf, self.textRect)
        self.display.blit(self.image, self.image_rect)

        if self.button:
            return True
        else:
            return False
