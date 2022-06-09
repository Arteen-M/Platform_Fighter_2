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
pygame.mixer.init()

HEIGHT = 600
WIDTH = 800
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Fighter")


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
def startScreen():
    # Other initializations, like frames and text
    frame_count = 0
    bigText = text.Text("Platform Fighter", font, 90, BLUE, (0, HEIGHT / 2), display)
    smallText = text.Text("Press Space to Start", font, 45, DARK_BLUE, (0, HEIGHT / 2 + 100), display)

    while True:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # If you press space, go to next
                if event.key == K_SPACE:
                    return "Character Select"
                # Enable fullscreen
                if event.key == K_F11:
                    pygame.display.toggle_fullscreen()

        # Animation on entry (change position and smear)
        if frame_count < 60:
            bigText.update(bigText.text, (((frame_count ** 2) / 9), (HEIGHT / 2)))
            smallText.update(smallText.text, (WIDTH - ((frame_count ** 2) / 9), (HEIGHT / 2 + 100)))
        # Stop Smearing, just draw it
        elif frame_count == 60:
            display.fill(BLACK)
            bigText.update(bigText.text, (((frame_count ** 2) / 9), (HEIGHT / 2)))
            smallText.update(smallText.text, (WIDTH - ((frame_count ** 2) / 9), (HEIGHT / 2 + 100)))

        if frame_count == 500:  # Move to the next page after a certain amount of time
            return "Character Select"

        # Draw them with their updated position
        bigText.draw()
        smallText.draw()

        frame_count += 1

        pygame.display.update()
        FramePerSec.tick(FPS)


# startScreen()
