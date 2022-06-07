import pygame
from pygame.locals import *
import sys
import time
import pandas as pd
from GUI_Elements import control_select
from GUI_Elements import name_dropdown
from GUI_Elements import button

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

inputList = [K_TAB, K_CLEAR, K_RETURN, K_PAUSE, K_SPACE, K_QUOTE, K_MINUS,
             K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_SEMICOLON, K_EQUALS, K_LEFTBRACKET,
             K_BACKSLASH, K_RIGHTBRACKET, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k,
             K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP0, K_KP1, K_KP2, K_KP3,
             K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS,
             K_KP_ENTER, K_KP_EQUALS, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RALT, K_LALT]


def text_objects(text, font, colour, center):
    textSurface = font.render(text, True, colour)
    textRect = textSurface.get_rect(center=center)
    return textSurface, textRect


def controlChange():
    names = name_dropdown.nameDrop((WIDTH / 2 - 100, 150), display)
    panel = control_select.controlPanel(display, controls=names.controls)
    back_button = button.Button(50, 50, 150, 50, None, None, None, display)
    textSurf, textRect = text_objects("Back", pygame.font.SysFont('impact', 36), WHITE, (100, 75))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                panel.get_pressed(True)
                back_button.get_pressed(True)
                names.get_pressed(True)
            else:
                panel.get_pressed(False)
                back_button.get_pressed(False)
                names.get_pressed(False)

        display.fill(BLACK)

        display.blit(textSurf, textRect)

        back_button.update()
        if back_button.pressed:
            return names.names

        if not names.pressed:
            panel.update()
        if names.update() is not None:
            panel.reInit(names.controls)

        names.saveControls(panel.returnControls())

        pygame.display.update()
        FramePerSec.tick(FPS)


# controlChange()
