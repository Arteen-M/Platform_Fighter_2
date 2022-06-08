# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
import pandas as pd
from Version_1.GUI_Elements import char_select
from Version_1.GUI_Elements import player_select
from Version_1.GUI_Elements import button
from Version_1.GUI_Elements import text
from Version_1.GUI_Elements.text import font
from Version_1.Pages import control_changes

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------

pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Fighter")


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
def characterSelect():
    # Variables for
    characters = ["", ""]
    skins = [None, None]
    current_skins = [None, None]
    P1_choosing = True

    # Button for choosing the square
    square_select = char_select.charButton((400, 200), "Square", display, RED)
    # Button for moving to the control menu
    controls = button.Button(50, 50, 50, 50, None, None, RED, display, image="../Images/Controls.png")

    # Read the file containing controls
    try:
        player_controls = pd.read_csv("../Names/Names.csv").to_dict()
        if 'Unnamed: 0' in list(player_controls.keys()):
            player_controls.pop('Unnamed: 0')  # Remove the extra control column
    except pd.errors.EmptyDataError:  # If there is an error
        # Set the player controls list manually
        player_controls = {"Player 1": {0: K_LEFT, 1: K_RIGHT, 2: K_UP, 3: K_DOWN, 4: K_h},
                           "Player 2": {0: K_a, 1: K_d, 2: K_w, 3: K_s, 4: K_t}}

        # Write the default to the file to avoid errors next time
        df = pd.DataFrame(player_controls)
        df.to_csv("../Names/Names.csv")

    # Player 1 Box
    p1_select = player_select.playerSelect(1, (200, 450), RED, display)
    # Player 2 Box
    p2_select = player_select.playerSelect(2, (600, 450), BLUE, display)

    # Instructions text
    proceed = text.Text("Press Enter to Proceed", font, 20, WHITE, (WIDTH/2, HEIGHT - 20), display)
    # Which player is choosing
    choose = text.Text("", font, 30, RED, (WIDTH / 2, 55), display)

    while True:
        # Whoever is choosing, display the appropriate text
        if P1_choosing:
            choose.update(text="Player 1, Choose your Character:", color=RED)
        else:
            choose.update(text="Player 2, Choose your Character", color=BLUE)

        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # You can toggle fullscreen if you like
                if event.key == K_F11:
                    pygame.display.toggle_fullscreen()
                # Hit enter to continue
                if event.key == K_RETURN:
                    if characters[0] != "" and characters[1] != "":
                        # Return everything required
                        return "Game", characters, current_skins, player_controls

            # If you click down
            if event.type == MOUSEBUTTONDOWN:
                # Set all the buttons pressed functions to True
                p1_select.get_pressed(True)
                p2_select.get_pressed(True)
                square_select.get_pressed(True)
                controls.get_pressed(True)
            else:
                # If you aren't clicking down, set them all to false
                p1_select.get_pressed(False)
                p2_select.get_pressed(False)
                square_select.get_pressed(False)
                controls.get_pressed(False)

        # Clear the screen
        display.fill(BLACK)
        # Draw the text
        choose.draw()

        # Update (Draw) the buttons
        controls.update()
        square_select.update()

        # If both characters are chosen, then display the text to continue
        if characters[0] != "" and characters[1] != "":
            proceed.draw()  # Draw the text

        # If the control button is pressed
        if controls.pressed:
            # Move to the control menu
            player_controls = control_changes.controlChange()
            # Make sure the button isn't pressed
            controls.pressed = False

        # Skins for both players
        current_skins = [p1_select.skin, p2_select.skin]

        # Available skins for both players
        square_skins_1 = [RED, BLUE, GREEN, YELLOW]
        square_skins_2 = [RED, BLUE, GREEN, YELLOW]

        # Change the available skins list based on the opponents skin choice
        if current_skins[1] in square_skins_1:
            square_skins_1.remove(current_skins[1])
        if current_skins[0] in square_skins_2:
            square_skins_2.remove(current_skins[0])

        # If the character select button is pressed
        if square_select.button.pressed:
            if P1_choosing:  # If P1 is choosing
                characters[0] = "Square"  # The character is square
                skins[0] = square_skins_1  # Set its skin
                P1_choosing = False  # P1 is no longer choosing
            else:  # Same thing but for P2
                characters[1] = "Square"
                skins[1] = square_skins_2
                P1_choosing = True

            # The button is not pressed
            square_select.button.pressed = False

        # Sets skins
        if P1_choosing and characters[0] == "Square":
            skins[0] = square_skins_1

        if not P1_choosing and characters[1] == "Square":
            skins[1] = square_skins_2

        # Update the player boxes
        p1_select.update(characters[0], skins[0])
        p2_select.update(characters[1], skins[1])

        pygame.display.update()
        FramePerSec.tick(FPS)


# characterSelect()
