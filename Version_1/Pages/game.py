# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
import time
from Version_1.Characters import square
from Version_1.Stage_Elements import floor
from Version_1.Stage_Elements import wall
from Version_1.Characters.Character_Elements import graphic
from Version_1.Stage_Elements import timer
from Version_1.Pages import pause
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
display = pygame.display.set_mode((WIDTH,  HEIGHT))
pygame.display.set_caption("Platform Fighter")


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
def gameLoop(characters, controls, skins, times=1, stocks=3):
    num_time = times  # Set the time
    stocks = stocks  # Set the stocks

    # Initialize the timer
    timerObj = timer.Timer(num_time, font, 36, WHITE, (WIDTH - 100, 100), display)

    if characters[0] == "Square":
        # Create a square character
        P1 = square.Square(display, color=skins[0], spawn_position=((WIDTH / 2) - 100, HEIGHT / 2), controls=list(controls["Player 1"].values()), stocks=stocks)
        P1_Graphic = graphic.Graphic(display, font, 36, (300, 500), skins[0], stocks=stocks)
    if characters[1] == "Square":
        # Create a square character
        P2 = square.Square(display, color=skins[1], spawn_position=((WIDTH / 2) + 100, HEIGHT / 2), controls=list(controls["Player 2"].values()), stocks=stocks)
        P2_Graphic = graphic.Graphic(display, font, 36, (500, 500), skins[1], side=False, stocks=stocks)

    # Initialize the floor
    mainFloor = floor.Floor(display, dimensions=(WIDTH / 2, 10), pos=(WIDTH / 2, 400))

    # Initialize the two walls
    mainLeftWall = wall.Wall(display, direction="LEFT", dimensions=(10, HEIGHT / 2), pos=(600, 546))
    mainRightWall = wall.Wall(display, direction="RIGHT", dimensions=(10, HEIGHT / 2), pos=(200, 546))

    # Floor group (needed for collision)
    hard_floors = pygame.sprite.Group()
    hard_floors.add(mainFloor)

    # Walls group (needed for collision)
    walls = pygame.sprite.Group()
    walls.add(mainLeftWall)
    walls.add(mainRightWall)

    # END CONDITIONS: P1 Loses, P2 Loses, Timeout
    while not (P1.end or P2.end or timerObj.time_out):
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Pressed keys for Jumping
            if event.type == pygame.KEYDOWN:
                if event.key == P1.up:
                    if not P1.frozen:
                        P1.tapped_up = True
                if event.key == P2.up:
                    if not P2.frozen:
                        P2.tapped_up = True
                # Pause menu
                if event.key == K_ESCAPE:
                    # Pause the game
                    if pause.Pause() == "Character Select":  # If the pause menu wants to get out, then return
                        return
                    timerObj.reInit()  # Reset the timer (Don't restart it though)

        display.fill(BLACK)  # Clear the screen

        # Update with floors, walls and hitboxes
        P1.update(hard_floors, walls, P2.active_hitboxes)
        P2.update(hard_floors, walls, P1.active_hitboxes)

        # Update the graphic with information
        P1_Graphic.update(P1.percentage, P1.stocks)
        P2_Graphic.update(P2.percentage, P2.stocks)

        # Draw the elements in the sprite groups
        for element in hard_floors:
            element.draw()

        for element in walls:
            element.draw()

        # update the timer
        timerObj.update()

        pygame.display.update()
        FramePerSec.tick(FPS)  # CAP AT 60 FPS

    time.sleep(2)  # Delay to allow everyone to process

# gameLoop()
