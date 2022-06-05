import pygame
from pygame.locals import *
import sys
import time
from GUI_Elements import char_select
from GUI_Elements import player_select

pygame.init()
pygame.mixer.init()

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


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def characterSelect():
    characters = ["", ""]
    skins = [None, None]
    current_skins = [None, None]

    square_skins = [RED, BLUE, GREEN, YELLOW]

    square_select = char_select.charButton((400, 200), "Square", display, RED)

    p1_select = player_select.playerSelect(1, (200, 450), RED, display)
    p2_select = player_select.playerSelect(2, (600, 450), BLUE, display)

    while True:
        if characters[0] == "":
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
                        return characters, current_skins

        display.fill(BLACK)
        display.blit(textSurf, textRect)

        if square_select.update():
            if characters[0] == "":
                characters[0] = "Square"
                skins[0] = square_skins
                time.sleep(0.25)
            else:
                characters[1] = "Square"
                skins[1] = square_skins
                time.sleep(0.25)

        current_skins = [p1_select.skin, p2_select.skin]

        square_skins = [RED, BLUE, GREEN, YELLOW]
        if current_skins[0] in square_skins:
            square_skins.remove(current_skins[0])
        if current_skins[1] in square_skins:
            square_skins.remove(current_skins[1])

        p1_select.update(characters[0], skins[0])
        p2_select.update(characters[1], skins[1])

        pygame.display.update()
        FramePerSec.tick(FPS)
