# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
from Version_1.GUI_Elements import control_select
from Version_1.GUI_Elements import name_dropdown
from Version_1.GUI_Elements import button
from Version_1.GUI_Elements import text
from Version_1.GUI_Elements.text import font

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform_Fighter")


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
def controlChange():
    # Names (For now only P1 and P2, but more could be added later)
    names = name_dropdown.nameDrop((WIDTH / 2 - 100, 150), display)
    # Control panel (all the buttons to change controls)
    panel = control_select.controlPanel(display, controls=names.controls)
    # The back button
    back_button = button.Button(50, 50, 150, 50, None, None, None, display)
    # The back button text
    backText = text.Text("Back", font, 36, WHITE, (100, 75), display)

    while True:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If clicked
            if event.type == MOUSEBUTTONDOWN:
                panel.get_pressed(True)
                back_button.get_pressed(True)
                names.get_pressed(True)
            else:
                panel.get_pressed(False)
                back_button.get_pressed(False)
                names.get_pressed(False)

        # Clear the Screen
        display.fill(BLACK)

        # Draws the text
        backText.draw()

        # Updates the back button
        back_button.update()
        if back_button.pressed:
            # If it's pressed
            return names.names

        # If you aren't choosing a name
        if not names.pressed:
            # Update the panel
            panel.update()
        if names.update() is not None:
            # Change the panel when you change the name
            panel.reInit(names.controls)

        # Save the controls to the csv file (Every frame so your progress saves even if you don't finish)
        names.saveControls(panel.returnControls())

        pygame.display.update()
        FramePerSec.tick(FPS)


# controlChange()
