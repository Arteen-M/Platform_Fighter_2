import pygame
from pygame.locals import *
import sys
from Version_1.GUI_Elements import text
from Version_1.GUI_Elements.text import font

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
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Fighter")


def startScreen():
    intro = True
    frame_count = 0
    bigText = text.Text("Platform Fighter", font, 90, BLUE, (0, HEIGHT / 2), display)
    smallText = text.Text("Press Space to Start", font, 45, DARK_BLUE, (0, HEIGHT / 2 + 100), display)

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

        display.fill(BLACK)
        if frame_count < 60:
            frame_count += 1

        bigText.update(bigText.text, (((frame_count ** 2) / 9), (HEIGHT / 2)))
        smallText.update(smallText.text, (WIDTH - ((frame_count ** 2) / 9), (HEIGHT / 2 + 100)))

        bigText.draw()
        smallText.draw()

        pygame.display.update()
        FramePerSec.tick(FPS)

    return "Character Select"


# startScreen()
