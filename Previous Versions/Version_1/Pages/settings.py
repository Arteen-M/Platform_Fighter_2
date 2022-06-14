# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys
from Version_1.GUI_Elements import text
from Version_1.GUI_Elements.text import font
from Version_1.GUI_Elements import button

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()

HEIGHT = 600
WIDTH = 800
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)

FPS = 60
FramePerSec = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform_Fighter")


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
def Settings(time, stocks):
    # Header
    header = text.Text("Settings", font, 56, WHITE, (WIDTH / 2, 100), display)

    # Times variables
    times_int = time  # Time (int)
    times_str = str(time) + ":00"  # Time (str)
    timeHeader = text.Text("Time", font, 36, WHITE, (WIDTH / 3, HEIGHT / 2 - 100), display)  # Header
    timeText = text.Text(times_str, font, 26, WHITE, (WIDTH / 3, HEIGHT / 2 - 50), display)  # Actual time text

    # Stocks variable
    stock = stocks  # Stocks (int)
    stocksHeader = text.Text("Stocks", font, 36, WHITE, (2 * WIDTH / 3, HEIGHT / 2 - 100), display)  # Header
    stocksText = text.Text(str(stock), font, 26, WHITE, (2 * WIDTH / 3, HEIGHT / 2 - 50), display)  # Actual Stock text

    # Increase time button
    timeUp = button.Button(WIDTH / 3 + 38, HEIGHT / 2 - 80, 25, 25, ((WIDTH / 3 + 40, HEIGHT / 2 - 60), (WIDTH / 3 + 60, HEIGHT / 2 - 60), (WIDTH / 3 + 50, HEIGHT / 2 - 80)), GRAY, RED, display, draw=True)
    # Decrease time button
    timeDown = button.Button(WIDTH / 3 + 38, HEIGHT / 2 - 42, 25, 25, ((WIDTH / 3 + 40, HEIGHT / 2 - 40), (WIDTH / 3 + 60, HEIGHT / 2 - 40), (WIDTH / 3 + 50, HEIGHT / 2 - 20)), GRAY, RED, display, draw=True)

    # Increase stocks button
    stockUp = button.Button(2 * WIDTH / 3 + 38, HEIGHT / 2 - 80, 25, 25, ((2 * WIDTH / 3 + 40, HEIGHT / 2 - 60), (2 * WIDTH / 3 + 60, HEIGHT / 2 - 60), (2 * WIDTH / 3 + 50, HEIGHT / 2 - 80)), GRAY, RED, display, draw=True)
    # Decrease stocks button
    stockDown = button.Button(2 * WIDTH / 3 + 38, HEIGHT / 2 - 42, 25, 25, ((2 * WIDTH / 3 + 40, HEIGHT / 2 - 40), (2 * WIDTH / 3 + 60, HEIGHT / 2 - 40), (2 * WIDTH / 3 + 50, HEIGHT / 2 - 20)), GRAY, RED, display, draw=True)

    back_button = button.Button(50, 50, 150, 50, None, None, None, display)
    # The back button text
    backText = text.Text("Back", font, 36, WHITE, (100, 75), display)

    while True:
        # Event loop
        display.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # Enable fullscreen
                if event.key == K_F11:
                    pygame.display.toggle_fullscreen()

            # Buttons pressed
            if event.type == MOUSEBUTTONDOWN:
                timeUp.get_pressed(True)
                timeDown.get_pressed(True)
                stockUp.get_pressed(True)
                stockDown.get_pressed(True)
                back_button.get_pressed(True)

        # Update the time up button
        timeUp.update()
        if timeUp.pressed:
            # increase the time
            times_int += 1
            times_str = str(times_int) + ":00"
            timeUp.pressed = False

        # Update the time down button
        timeDown.update()
        if timeDown.pressed:
            # decrease the time
            if times_int > 1:
                times_int -= 1
            times_str = str(times_int) + ":00"
            timeDown.pressed = False

        # Update the stock up button
        stockUp.update()
        if stockUp.pressed:
            # increase the stocks
            stock += 1
            stockUp.pressed = False

        # Update the stock down button
        stockDown.update()
        if stockDown.pressed:
            # decrease the stocks
            if stock > 1:
                stock -= 1
            stockDown.pressed = False

        # update both texts
        timeText.update(times_str)
        stocksText.update(str(stock))

        # Return the time and stocks
        if back_button.pressed:
            return times_int, stock

        # Draw all the texts
        header.draw()
        timeHeader.draw()
        timeText.draw()
        stocksHeader.draw()
        stocksText.draw()
        backText.draw()

        pygame.display.update()
        FramePerSec.tick(FPS)


# Settings(3, 3)
