import pygame


class Button:
    def __init__(self, x, y, w, h, shape, fill_color, border_color, display, rect=False, draw=False, border=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.shape = shape

        self.solid_color = fill_color
        self.border_color = border_color

        self.rect = rect
        self.draw = draw
        self.border = border

        self.pressed = False

        self.display = display

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            if click[0] == 1:
                self.pressed = True
                return True
            else:
                self.pressed = False

        if self.draw:
            if self.rect:
                pygame.draw.rect(self.display, self.solid_color, (self.x, self.y, self.w, self.h))
                if self.border:
                    pygame.draw.rect(self.display, self.border_color, (self.x, self.y, self.w, self.h), 1)
            else:
                pygame.draw.polygon(self.display, self.solid_color, self.shape)
        elif self.border:
            if self.rect:
                pygame.draw.rect(self.display, self.border_color, (self.x, self.y, self.w, self.h), 1)
            else:
                pygame.draw.polygon(self.display, self.border_color, self.shape, 1)


