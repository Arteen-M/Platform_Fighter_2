# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
import math
from Platform_Fighter.path import path
from Platform_Fighter.GUI_Elements import text


# -------------------------------------------------------------------------
# Class Definition
# -------------------------------------------------------------------------
class Graphic:
    def __init__(self, display, font, size, pos, color, stocks=3, img=None, scale=None):
        # Percentage Text
        self.text = "0%"
        self.font = font
        self.pos = pos
        self.color = color
        self.display = display
        self.total_stocks = stocks  # Total stocks and stocks are independent
        self.stocks = 0
        self.flash_image = pygame.transform.scale(pygame.image.load(path + "Images/Stickman/Flash/flash_image.png"), (93, 100))
        self.flash_image_rect = self.flash_image.get_rect(midbottom=(self.pos[0] - 3, self.pos[1] + 20))
        if img is not None:
            # if the stock graphic is an image rather than a square
            self.image = pygame.transform.scale(pygame.image.load(img), scale).convert_alpha()
        else:
            self.image = None

        # Text for the percentage
        self.textGraphic = text.Text(self.text, self.font, size, self.color, self.pos, self.display)

    # Update the graphic
    def update(self, percentage, stocks, flash_percent):
        self.stocks = stocks  # Update the stocks
        self.text = str(math.floor(percentage)) + "%"  # Update the percentage

        pygame.draw.rect(self.display, (125, 125, 125), (self.pos[0] - 45, self.pos[1] - 45, 85, 85 + 15 * ((self.total_stocks-1)//3)))
        pygame.draw.rect(self.display, (0, 0, 0), (self.pos[0] - 45, self.pos[1] - 45, 85, 85 + 15 * ((self.total_stocks-1)//3)), 1)

        self.textGraphic.update(text=self.text)  # Update the text with the new percentage
        self.textGraphic.draw()  # Draw the text

        if flash_percent < 100:
            pygame.draw.rect(self.display, self.color, (self.pos[0] - 44, self.pos[1] - 40, 84 / 100 * flash_percent, 20))
        else:
            pygame.draw.rect(self.display, (255, 255, 0), (self.pos[0] - 44, self.pos[1] - 40, 84 / 100 * flash_percent, 20))
        self.display.blit(self.flash_image, self.flash_image_rect)

        # If the graphic is not an image (square)
        if self.image is None:
            # Display each square depending on the number of stocks
            for num in range(self.stocks):
                pygame.draw.rect(self.display, self.color,
                                 (self.pos[0] - 25 + (15 * (num % 3)), self.pos[1] + 20 + (15 * (num // 3)), 10, 10))
        else:
            for num in range(self.stocks):
                self.display.blit(self.image, self.image.get_rect(center=(self.pos[0] - 30 + (26 * (num % 3)), self.pos[1] + 26 + (15 * (num // 3)))))

            # for num in range(self.stocks): pygame.draw.rect(self.display, self.color, (self.pos[0] + self.side,
            # self.pos[1] - 55 + (40 * num), 30, 30))
