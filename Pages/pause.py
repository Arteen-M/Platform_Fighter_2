import pygame
from pygame.locals import *
import sys

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


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def Pause():
    pauseSurf, pauseRect = text_objects("Pause", pygame.font.SysFont(font, 64), WHITE)
    pauseRect.center = (WIDTH/2, HEIGHT/2 - 50)

    instructSurf, instructRect = text_objects("Press Enter or Escape to Resume", pygame.font.SysFont(font, 32), WHITE)
    instructRect.center = (WIDTH/2, HEIGHT/2 + 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN or event.key == K_ESCAPE:
                    return

        display.fill(BLACK)
        display.blit(pauseSurf, pauseRect)
        display.blit(instructSurf, instructRect)

        pygame.display.update()
        FramePerSec.tick(FPS)
