import pygame
from pygame.locals import *
import sys
import time
from GUI_Elements import char_select
from GUI_Elements import player_select
import pandas as pd

pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)

FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Fighter")

font = 'impact'

data = pd.read_csv("../Names/Names.csv").to_dict()
data.pop("Unnamed: 0")
data.pop('Controls')


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def characterSelect():
    characters = ["", ""]
    skins = [None, None]
    current_skins = [None, None]
    P1_choosing = True

    square_skins = [RED, BLUE, GREEN, YELLOW]
    square_skins_1 = [RED, BLUE, GREEN, YELLOW]
    square_skins_2 = [RED, BLUE, GREEN, YELLOW]

    square_select = char_select.charButton((400, 200), "Square", display, RED)

    p1_select = player_select.playerSelect(1, (200, 450), RED, display)
    p2_select = player_select.playerSelect(2, (600, 450), BLUE, display)

    surf, rect = text_objects("Press Enter to Proceed", pygame.font.SysFont(font, 20), WHITE)
    rect.center = (WIDTH/2, HEIGHT - 20)

    while True:
        if P1_choosing:
            textSurf, textRect = text_objects("Player 1, Choose your Character:", pygame.font.SysFont(font, 30), RED)
        else:
            textSurf, textRect = text_objects("Player 2, Choose your Character:", pygame.font.SysFont(font, 30), BLUE)
        textRect.center = (WIDTH/2, 55)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F11:
                    pygame.display.toggle_fullscreen()
                if event.key == K_RETURN:
                    if characters[0] is not None and characters[1] is not None:
                        return "Game", characters, current_skins

        display.fill(BLACK)
        display.blit(textSurf, textRect)
        display.blit(surf, rect)

        current_skins = [p1_select.skin, p2_select.skin]

        square_skins_1 = [RED, BLUE, GREEN, YELLOW]
        square_skins_2 = [RED, BLUE, GREEN, YELLOW]

        if current_skins[1] in square_skins_1:
            square_skins_1.remove(current_skins[1])
        if current_skins[0] in square_skins_2:
            square_skins_2.remove(current_skins[0])

        if square_select.update():
            if P1_choosing:
                characters[0] = "Square"
                skins[0] = square_skins_1
                P1_choosing = False
                time.sleep(0.25)
            else:
                characters[1] = "Square"
                skins[1] = square_skins_2
                P1_choosing = True
                time.sleep(0.25)

        if P1_choosing and characters[0] == "Square":
            skins[0] = square_skins_1

        if not P1_choosing and characters[1] == "Square":
            skins[1] = square_skins_2

        p1_select.update(characters[0], skins[0])
        p2_select.update(characters[1], skins[1])

        pygame.display.update()
        FramePerSec.tick(FPS)


# characterSelect()
