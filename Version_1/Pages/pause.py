# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
from Version_1.GUI_Elements import text
from Version_1.GUI_Elements.text import font

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


def Pause():
    pauseText = text.Text("Pause", font, 64, WHITE, (WIDTH/2, HEIGHT/2 - 50), display)
    instructText = text.Text("Press Enter or Escape to Resume", font, 32, WHITE, (WIDTH/2, HEIGHT/2 + 50), display)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN or event.key == K_ESCAPE:
                    return

        display.fill(BLACK)
        pauseText.draw()
        instructText.draw()

        pygame.display.update()
        FramePerSec.tick(FPS)
