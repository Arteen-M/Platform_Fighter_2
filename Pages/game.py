import pygame
from pygame.locals import *
import sys
from Characters import square
from Stage_Elements import floor
from Stage_Elements import wall
from Characters.Character_Elements import graphic
from Stage_Elements import timer
from Pages import pause
import time

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

FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH,  HEIGHT))
pygame.display.set_caption("Platform Fighter")

font = "impact"


def gameLoop(characters, skins, times=1, stocks=3):
    num_time = times
    stocks = stocks

    timerObj = timer.Timer(num_time, font, 36, WHITE, (WIDTH - 100, 100), display)

    if characters[0] == "Square":
        P1 = square.Square(display, color=skins[0], spawn_position=((WIDTH/2) - 100, HEIGHT/2), stocks=stocks)
        P1_Graphic = graphic.Graphic(display, font, 36, (300, 500), skins[0], stocks=stocks)
    if characters[1] == "Square":
        P2 = square.Square(display, color=skins[1], spawn_position=((WIDTH/2) + 100, HEIGHT/2), controls=(K_a, K_d, K_w, K_s, K_t), stocks=stocks)
        P2_Graphic = graphic.Graphic(display, font, 36, (500, 500), skins[1], side=False, stocks=stocks)

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
                if event.key == K_ESCAPE:
                    pause.Pause()

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
