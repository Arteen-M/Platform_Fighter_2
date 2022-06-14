# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
WIDTH = 800
HEIGHT = 600
GREEN = (0, 255, 0)


# -------------------------------------------------------------------------
# Class Definitions
# -------------------------------------------------------------------------
class Wall(pygame.sprite.Sprite):  # Inherit from sprite class
    def __init__(self, display, direction="LEFT", dimensions=(20, 100), pos=(WIDTH/2, HEIGHT/2), color=GREEN):
        super().__init__()
        self.surf = pygame.Surface(dimensions)  # Surface of the wall
        self.rect = self.surf.get_rect(center=pos)  # Rect (Position) of the wall

        self.color = color  # Color of the wall
        self.surf.fill(self.color)  # Background is filled

        self.display = display  # Display for drawing

        self.direction = direction  # Direction which the wall blocks (Right or left)

    # Draw the wall
    def draw(self):
        self.display.blit(self.surf, self.rect)
