import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.mixer.init()

HEIGHT = 600
WIDTH = 800
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
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Fighter")


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def startScreen():
    intro = True
    frame_count = 0

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    intro = False
                if event.key == K_F11:
                    pygame.display.toggle_fullscreen()

        displaysurface.fill(BLACK)
        if frame_count < 60:
            frame_count += 1

        largeText = pygame.font.SysFont('impact', 90)
        smallText = pygame.font.SysFont('impact', 45)

        TextSurf, TextRect = text_objects("Platform Fighter", largeText, BLUE)
        smallTextSurf, smallTextRect = text_objects("Press Space to Start", smallText, DARK_BLUE)

        TextRect.center = (((frame_count ** 2) / 9), (HEIGHT / 2))
        smallTextRect.center = (WIDTH - ((frame_count ** 2) / 9), (HEIGHT / 2 + 100))

        displaysurface.blit(TextSurf, TextRect)
        displaysurface.blit(smallTextSurf, smallTextRect)

        pygame.display.update()
        FramePerSec.tick(FPS)

    return "Character Select"


# startScreen()
