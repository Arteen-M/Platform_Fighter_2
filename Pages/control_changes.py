import pygame
from pygame.locals import *
import sys
from GUI_Elements import control_select
from GUI_Elements import name_dropdown

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


panel = control_select.controlPanel(display)
names = name_dropdown.nameDrop((WIDTH/2 - 100, 150), display)


def button(x, y, w, h, display):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    text = text_objects("Back", pygame.font.SysFont(font, 36), WHITE, (x + w/2, y + h/2))

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1:
            return True

    display.blit(text[0], text[1])
    pygame.draw.rect(display, RED, (x, y, w, h), 1)


def controlChange():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display.fill(BLACK)
        if button(50, 50, 150, 50, display):
            return "Character Select"

        if not names.pressed:
            panel.update()
        if names.update() is not None:
            panel.reInit(names.controls)

        names.saveControls(panel.returnControls())

        pygame.display.update()
        FramePerSec.tick(FPS)


controlChange()
