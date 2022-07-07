import pygame
from Platform_Fighter.GUI_Elements import button


class checkBox:
    def __init__(self, size, pos, outline, fill, display):
        self.button = button.Button(pos[0], pos[1], size[0], size[1], None, None, outline, display, False, True, True)
        self.pressed = False
        self.rect = (pos[0], pos[1], size[0], size[1])
        self.display = display
        self.fill_color = fill

    def update(self):
        self.button.update()
        if self.button.pressed:
            self.button.pressed = False
            if self.pressed:
                self.pressed = False
            else:
                self.pressed = True

        if self.pressed:
            pygame.draw.rect(self.display, self.fill_color, self.rect)

    def get_pressed(self, click):
        self.button.get_pressed(click)

