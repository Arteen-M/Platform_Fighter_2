# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
import time
from Platform_Fighter.Characters import square
from Platform_Fighter.Characters import stickman
from Platform_Fighter.Stage_Elements import floor
from Platform_Fighter.Stage_Elements import wall
from Platform_Fighter.Characters.Character_Elements import graphic
from Platform_Fighter.Stage_Elements import timer
from Platform_Fighter.Pages import pause
from Platform_Fighter.GUI_Elements.text import font, Text
from Platform_Fighter.Stage_Elements import background
from Platform_Fighter.path import path

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
vec = pygame.math.Vector2
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(3)

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)
BLUE = (0, 0, 255)
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
    elif characters[0] == "Stickman":
        P1 = stickman.Stickman(display, color=RED, spawn_position=((WIDTH / 2) - 100, HEIGHT / 2), controls=list(controls["Player 1"].values()), stocks=stocks)
        P1_Graphic = graphic.Graphic(display, font, 36, (275, 500), RED, stocks=stocks, img=path+"Images/Stickman/stick_stock_graphic.png", scale=(80, 80))
    else:
        raise Exception("No Character Selected. How did you do that?")

    if characters[1] == "Square":
        # Create a square character
        P2 = square.Square(display, color=skins[1], spawn_position=((WIDTH / 2) + 100, HEIGHT / 2), controls=list(controls["Player 2"].values()), stocks=stocks)
        P2_Graphic = graphic.Graphic(display, font, 36, (525, 500), skins[1], stocks=stocks)
    elif characters[1] == "Stickman":
        P2 = stickman.Stickman(display, color=BLUE, spawn_position=((WIDTH / 2) + 100, HEIGHT / 2), controls=list(controls["Player 2"].values()), stocks=stocks)
        P2_Graphic = graphic.Graphic(display, font, 36, (525, 500), BLUE, stocks=stocks, img=path + "Images/Stickman/stick_stock_graphic.png", scale=(80, 80))
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

    bg = background.Background(path+"Images/Background/frames/", 20, 8, display)

    musicObj = pygame.mixer.Sound(path+"Music/PlatformBanger2 (3).wav")
    musicObj.set_volume(0.5)
    musicObj.play(-1)

    P1HitMusic = pygame.mixer.Sound(path+"Music/HitSfX.wav")
    P2HitMusic = pygame.mixer.Sound(path+"Music/HitSfX.wav")

    P1ShieldMusic = pygame.mixer.Sound(path+"Music/shield7.wav")
    P2ShieldMusic = pygame.mixer.Sound(path + "Music/shield7.wav")

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

        """
        key_pressed = pygame.key.get_pressed()
        for x in range(len(P1.controls)):
            if key_pressed[P1.controls[x]]:
                if x == 0:
                    P1.left_bool = True
                if x == 1:
                    P1.right_bool = True
                if x == 2:
                    P1.up_bool = True
                if x == 3:
                    P1.down_bool = True
                if x == 4:
                    P1.attack_bool = True
                if x == 5:
                    P1.shield_bool = True
                if x == 6:
                    P1.special_bool = True

        for x in range(len(P2.controls)):
            if key_pressed[P2.controls[x]]:
                if x == 0:
                    P2.left_bool = True
                elif x == 1:
                    P2.right_bool = True
                elif x == 2:
                    P2.up_bool = True
                elif x == 3:
                    P2.down_bool = True
                elif x == 4:
                    P2.attack_bool = True
                elif x == 5:
                    P2.shield_bool = True
                elif x == 6:
                    P2.special_bool = True
        """

        # Update with floors, walls and hitboxes
        P1.update(hard_floors, soft_floors, under_floors, walls, P2.active_hitboxes, P2.shield_box)
        P2.update(hard_floors, soft_floors, under_floors, walls, P1.active_hitboxes, P1.shield_box)

        if P1.got_hit:
            P2HitMusic.play()
            if P1.box.name != "Projectile":
                P2.hitconfirm = P1.hitstop

            if P2.flash_percent < 90:
                P2.flash_percent += 10
            else:
                P2.flash_percent = 100

        if P1.got_shield:
            P1ShieldMusic.play()
            xBack = abs(P1.knockbackFormula(P1.shield_hit.x_component, P1.shield_hit.damage, P1.shield_hit.knockback_scale,
                                                     P1.shield_hit.base_knockback, 1))
            if not P1.direction:
                xBack *= -1

            P2.vel.x = xBack

            P2.hitconfirm = P1.findHitstop(P1.shield_hit.damage, 0.75)
            P1.hitconfirm = P1.findHitstop(P1.shield_hit.damage, 0.75)

        if P2.got_hit:
            P1HitMusic.play()
            if P2.box.name != "Projectile":
                P1.hitconfirm = P2.hitstop

            if P1.flash_percent < 90:
                P1.flash_percent += 10
            else:
                P1.flash_percent = 100

        if P2.got_shield:
            P2ShieldMusic.play()

            xBack = abs(P1.knockbackFormula(P2.shield_hit.x_component, P2.shield_hit.damage, P2.shield_hit.knockback_scale,
                                                     P2.shield_hit.base_knockback, 1))
            if not P2.direction:
                xBack *= -1

            P1.vel.x = xBack

            P2.hitconfirm = P1.findHitstop(P2.shield_hit.damage, 0.75)
            P1.hitconfirm = P1.findHitstop(P2.shield_hit.damage, 0.75)

        # Update the graphic with information
        P1_Graphic.update(P1.percentage, P1.stocks, P1.flash_percent)
        P2_Graphic.update(P2.percentage, P2.stocks, P2.flash_percent)

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
    time.sleep(2)  # Delay, to allow everyone to process

    return

# gameLoop()