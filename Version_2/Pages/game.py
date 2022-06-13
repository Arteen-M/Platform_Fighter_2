# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
import time
from Version_2.Characters import square
from Version_2.Stage_Elements import floor
from Version_2.Stage_Elements import wall
from Version_2.Characters.Character_Elements import graphic
from Version_2.Stage_Elements import timer
from Version_2.Pages import pause
from Version_2.GUI_Elements.text import font, Text
from Version_2.Stage_Elements import background

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(3)

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH,  HEIGHT))
pygame.display.set_caption("Platform Fighter")


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
def gameLoop(characters, controls, skins, times=3, stock=3, debug=False):
    num_time = times  # Set the time
    stocks = stock  # Set the stocks

    # Initialize the timer
    timerObj = timer.Timer(num_time, font, 36, BLACK, (WIDTH - 100, 100), display)
    fpsObj = Text("0.0", font, 20, BLACK, (WIDTH - 100, 135), display)

    if characters[0] == "Square":
        # Create a square character
        P1 = square.Square(display, color=skins[0], spawn_position=((WIDTH / 2) - 100, HEIGHT / 2), controls=list(controls["Player 1"].values()), stocks=stocks)
        P1_Graphic = graphic.Graphic(display, font, 36, (275, 500), skins[0], stocks=stocks)
    else:
        raise Exception("No Character Selected. How did you do that?")

    if characters[1] == "Square":
        # Create a square character
        P2 = square.Square(display, color=skins[1], spawn_position=((WIDTH / 2) + 100, HEIGHT / 2), controls=list(controls["Player 2"].values()), stocks=stocks)
        P2_Graphic = graphic.Graphic(display, font, 36, (525, 500), skins[1], stocks=stocks)
    else:
        raise Exception("No Character Selected. How did you do that?")

    # Initialize the floor
    mainFloor = floor.Floor(display, dimensions=(WIDTH/2, 10), pos=(WIDTH / 2, 418))

    lPlat1 = floor.Floor(display, dimensions=(70, 6), pos=(236, 337))
    underlPlat1 = floor.Floor(display, dimensions=(70, 1), pos=(236, 342), color=RED)

    lPlat2 = floor.Floor(display, dimensions=(70, 6), pos=(564, 337))
    underlPlat2 = floor.Floor(display, dimensions=(70, 1), pos=(564, 342), color=RED)

    uPlat1 = floor.Floor(display, dimensions=(50, 6), pos=(349, 275))
    underuPlat1 = floor.Floor(display, dimensions=(50, 1), pos=(349, 280), color=RED)

    uPlat2 = floor.Floor(display, dimensions=(50, 6), pos=(451, 275))
    underuPlat2 = floor.Floor(display, dimensions=(50, 1), pos=(451, 280), color=RED)

    # Initialize the two walls
    mainLeftWall = wall.Wall(display, direction="LEFT", dimensions=(10, HEIGHT / 2), pos=(600, 564))
    mainRightWall = wall.Wall(display, direction="RIGHT", dimensions=(10, HEIGHT / 2), pos=(200, 564))

    # Floor group (needed for collision)
    hard_floors = pygame.sprite.Group()
    hard_floors.add(mainFloor)

    soft_floors = pygame.sprite.Group()
    soft_floors.add(lPlat1)
    soft_floors.add(lPlat2)
    soft_floors.add(uPlat1)
    soft_floors.add(uPlat2)

    under_floors = pygame.sprite.Group()
    under_floors.add(underlPlat1)
    under_floors.add(underlPlat2)
    under_floors.add(underuPlat1)
    under_floors.add(underuPlat2)

    # Walls group (needed for collision)
    walls = pygame.sprite.Group()
    walls.add(mainLeftWall)
    walls.add(mainRightWall)

    bg = background.Background("../Images/Background/frames/", 20, 8, display)

    musicObj = pygame.mixer.Sound("../Music/PlatformBanger2 (3).wav")
    musicObj.play(-1)

    P1HitMusic = pygame.mixer.Sound("../Music/HitSfX.wav")
    P2HitMusic = pygame.mixer.Sound("../Music/HitSfX.wav")

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
                        musicObj.stop()
                        return
                    timerObj.reInit()  # Reset the timer (Don't restart it though)

        # display.fill(BLACK)  # Clear the screen
        bg.update()

        # Update with floors, walls and hitboxes
        P1.update(hard_floors, soft_floors, under_floors, walls, P2.active_hitboxes)
        P2.update(hard_floors, soft_floors, under_floors, walls, P1.active_hitboxes)

        if P1.got_hit:
            P2HitMusic.play()

        if P2.got_hit:
            P1HitMusic.play()

        # Update the graphic with information
        P1_Graphic.update(P1.percentage, P1.stocks)
        P2_Graphic.update(P2.percentage, P2.stocks)

        # Draw all debug elements
        if debug:
            for element in P1.all_hitboxes:
                if element.active:
                    element.draw()

            for element in P2.all_hitboxes:
                if element.active:
                    element.draw()

            for element in hard_floors:
                element.draw()

            for element in soft_floors:
                element.draw()

            for element in under_floors:
                element.draw()

            for element in walls:
                element.draw()

            fpsObj.update(str(round(FramePerSec.get_fps(), 2)))
            fpsObj.draw()

        # update the timer
        timerObj.update()

        pygame.display.update()
        FramePerSec.tick(FPS)  # CAP AT 60 FPS

    musicObj.stop()
    time.sleep(2)  # Delay to allow everyone to process

# gameLoop()
