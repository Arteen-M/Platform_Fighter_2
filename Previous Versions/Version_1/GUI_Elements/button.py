# -------------------------------------------------------------------------
# IMPORT
# -------------------------------------------------------------------------
import pygame


# -------------------------------------------------------------------------
# Class Definition
# -------------------------------------------------------------------------
class Button:
    def __init__(self, x, y, w, h, shape, fill_color, border_color, display, rect=False, draw=False, border=False, image=None):
        self.x = x
        self.y = y  # Position
        self.w = w  # Variables
        self.h = h

        self.shape = shape  # Shape if not a rectangle

        # Colors
        self.solid_color = fill_color
        self.border_color = border_color

        # What to draw variables
        self.rect = rect
        self.draw = draw
        self.border = border

        # Drawing Images
        if image is not None:
            self.image = pygame.transform.scale(pygame.image.load(image), (self.w, self.h))
            self.image_rect = self.image.get_rect(center=(self.x + (self.w/2), self.y + (self.h/2)))
        else:
            self.image = None

        # Button pressed variable
        self.pressed = False

        # Display
        self.display = display

    # Draw (used to be used for pressed button, but that was changed)
    def update(self):
        if self.draw:
            if self.rect:
                pygame.draw.rect(self.display, self.solid_color, (self.x, self.y, self.w, self.h))
                if self.border:
                    pygame.draw.rect(self.display, self.border_color, (self.x, self.y, self.w, self.h), 1)
            else:
                pygame.draw.polygon(self.display, self.solid_color, self.shape)

        if self.border:
            pygame.draw.rect(self.display, self.border_color, (self.x, self.y, self.w, self.h), 1)

        if self.image is not None:
            self.display.blit(self.image, self.image_rect)

    # Change the pressed state of the button
    def get_pressed(self, click):
        mouse = pygame.mouse.get_pos()

        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            if click:
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.pressed = False


