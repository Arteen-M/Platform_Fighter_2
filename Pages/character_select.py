import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
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

characters = ["", ""]
P1_chosen = False


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


while True:
    if not P1_chosen:
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

    display.fill(BLACK)
    display.blit(textSurf, textRect)

    pygame.display.update()
    FramePerSec.tick(FPS)
