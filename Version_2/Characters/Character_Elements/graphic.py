# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
import math
from Version_2.GUI_Elements import text


# -------------------------------------------------------------------------
# Class Definition
# -------------------------------------------------------------------------
class Graphic:
    def __init__(self, display, font, size, pos, color, stocks=3, img=None):
        # Percentage Text
        self.text = "0%"
        self.font = font
        self.pos = pos
        self.color = color
        self.display = display
        self.total_stocks = stocks  # Total stocks and stocks are independent
        self.stocks = 0
        self.image = img  # if the stock graphic is an image rather than a square

        # Text for the percentage
        self.textGraphic = text.Text(self.text, self.font, size, self.color, self.pos, self.display)

    # Update the graphic
    def update(self, percentage, stocks):
        self.stocks = stocks  # Update the stocks
        self.text = str(math.floor(percentage)) + "%"  # Update the percentage

        pygame.draw.rect(self.display, (125, 125, 125), (self.pos[0] - 45, self.pos[1] - 25, 85, 65 + 15 * ((self.total_stocks-1)//3)))
        pygame.draw.rect(self.display, (0, 0, 0), (self.pos[0] - 45, self.pos[1] - 25, 85, 65 + 15 * ((self.total_stocks-1)//3)), 1)

        self.textGraphic.update(text=self.text)  # Update the text with the new percentage
        self.textGraphic.draw()  # Draw the text

        # If the graphic is not an image (square)
        if self.image is None:
            # Display each square depending on the number of stocks
            for num in range(self.stocks):
                pygame.draw.rect(self.display, self.color,
                                 (self.pos[0] - 25 + (15 * (num % 3)), self.pos[1] + 20 + (15 * (num // 3)), 10, 10))
            # for num in range(self.stocks): pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side,
            # self.pos[1] - 55 + (40 * num), 30, 30))
