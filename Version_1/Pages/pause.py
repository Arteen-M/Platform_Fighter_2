# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
from Version_1.GUI_Elements import text
from Version_1.GUI_Elements.text import font

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform_Fighter")


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
def Pause():
    # Texts for instructions
    pauseText = text.Text("Pause", font, 64, WHITE, (WIDTH/2, HEIGHT/2 - 50), display)
    resumeText = text.Text("Press Enter to Resume", font, 32, WHITE, (WIDTH/2, HEIGHT/2 + 50), display)
    escapeText = text.Text("Press Escape to Exit", font, 26, WHITE, (WIDTH/2, HEIGHT/2+85), display)

    # Draw Everything (Just once)
    display.fill(BLACK)
    pauseText.draw()
    resumeText.draw()
    escapeText.draw()

    while True:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:  # Return to the game
                    return "Game"
                if event.key == K_ESCAPE:  # Go back to character select
                    return "Character Select"

        pygame.display.update()
        FramePerSec.tick(FPS)
