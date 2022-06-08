import pygame
import math
from Version_1.GUI_Elements import text


class Graphic:
    def __init__(self, display, font, size, pos, color, side=True, stocks=3, img=None):
        self.text = "0%"
        self.font = font
        self.pos = pos
        self.color = color
        self.display = display
        self.total_stocks = stocks
        self.stocks = 0
        if side:
            self.side = -70
        else:
            self.side = 40
        self.image = img

        self.textGraphic = text.Text(self.text, self.font, size, self.color, self.pos, self.display)

    def update(self, percentage, stocks):
        self.stocks = stocks
        self.text = str(math.floor(percentage)) + "%"

        self.textGraphic.update(text=self.text)
        self.textGraphic.draw()

        if self.image is None:
            for num in range(self.stocks):
                pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side, self.pos[1] - 55 + (40 * num), 30, 30))



