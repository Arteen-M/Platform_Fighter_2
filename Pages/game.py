import pygame
from pygame.locals import *
import sys
from Characters import square
from Stage_Elements import floor
from Stage_Elements import wall
from Characters.Character_Elements import graphic
from Stage_Elements import timer
import time
import pandas as pd

pygame.init()
pygame.font.init()


WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)

inputList = [K_TAB, K_CLEAR, K_RETURN, K_PAUSE, K_SPACE, K_QUOTE, K_MINUS,
             K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_SEMICOLON, K_EQUALS, K_LEFTBRACKET,
             K_BACKSLASH, K_RIGHTBRACKET, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k,
             K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP0, K_KP1, K_KP2, K_KP3,
             K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS,
             K_KP_ENTER, K_KP_EQUALS, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RALT, K_LALT]

FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH,  HEIGHT))
pygame.display.set_caption("Platform Fighter")

font = "impact"


def gameLoop(times=1, stocks=3):
    num_time = times
    stocks = stocks

    timerObj = timer.Timer(num_time, font, 36, WHITE, (WIDTH - 100, 100), display)

    P1 = square.Square(display, color=RED, spawn_position=((WIDTH/2) - 100, HEIGHT/2), stocks=stocks)
    P1_Graphic = graphic.Graphic(display, font, 36, (300, 500), RED, stocks=stocks)
    P2 = square.Square(display, color=BLUE, spawn_position=((WIDTH/2) + 100, HEIGHT/2), controls=(K_a, K_d, K_w, K_s, K_t), stocks=stocks)
    P2_Graphic = graphic.Graphic(display, font, 36, (500, 500), BLUE, side=False, stocks=stocks)

    mainFloor = floor.Floor(display, dimensions=(WIDTH/2, 10), pos=(WIDTH/2, 400))

    mainLeftWall = wall.Wall(display, direction="LEFT", dimensions=(10, HEIGHT/2), pos=(600, 546))
    mainRightWall = wall.Wall(display, direction="RIGHT", dimensions=(10, HEIGHT/2), pos=(200, 546))

    hard_floors = pygame.sprite.Group()
    hard_floors.add(mainFloor)

    walls = pygame.sprite.Group()
    walls.add(mainLeftWall)
    walls.add(mainRightWall)

    while not (P1.end or P2.end or timerObj.time_out):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == P1.up:
                    if not P1.frozen:
                        P1.tapped_up = True
                if event.key == P2.up:
                    if not P2.frozen:
                        P2.tapped_up = True

        display.fill(BLACK)

        P1.update(hard_floors, walls, P2.active_hitboxes)
        P2.update(hard_floors, walls, P1.active_hitboxes)

        P1_Graphic.update(P1.percentage, P1.stocks)
        P2_Graphic.update(P2.percentage, P2.stocks)

        for element in hard_floors:
            element.draw()

        for element in walls:
            element.draw()

        timerObj.update(time.time())

        pygame.display.update()
        FramePerSec.tick(FPS)

# gameLoop()