# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
WIDTH = 800
HEIGHT = 600
BLUE = (0, 0, 255)


# -------------------------------------------------------------------------
# Class Definition
# -------------------------------------------------------------------------
class Floor(pygame.sprite.Sprite):  # Inherited from sprite class
    def __init__(self, display, dimensions=(100, 20), pos=(WIDTH/2, HEIGHT/2), color=BLUE):
        super().__init__()
        self.surf = pygame.Surface(dimensions)  # Floor surface
        self.rect = self.surf.get_rect(center=pos)  # Rect (position)

        self.color = color  # Color of the floor
        self.surf.fill(self.color)  # Optional once background is drawn

        self.display = display  # Display

    # Draw the floor (Optional)
    def draw(self):
        self.display.blit(self.surf, self.rect)
