import pygame
from pygame.locals import *
from GUI_Elements import button


font = 'impact'


input_list = [K_TAB, K_CLEAR, K_RETURN, K_PAUSE, K_SPACE, K_QUOTE, K_MINUS,
             K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_SEMICOLON, K_EQUALS, K_LEFTBRACKET,
             K_BACKSLASH, K_RIGHTBRACKET, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k,
             K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP0, K_KP1, K_KP2, K_KP3,
             K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS,
             K_KP_ENTER, K_KP_EQUALS, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RALT, K_LALT]

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
DARK_RED = (125, 0, 0)
DARKER_RED = (75, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


class controlButton:
    def __init__(self, name, control, pos, display, bigSize=32, smallSize=20):
        self.name = name
        self.control = control
        self.pos = pos

        self.bigFont = pygame.font.SysFont(font, bigSize)
        self.smallFont = pygame.font.SysFont(font, smallSize)

        self.nameSurf, self.nameRect = text_objects(self.name, self.bigFont, WHITE)
        self.nameRect.center = (self.pos[0], self.pos[1])

        self.controlSurf, self.controlRect = text_objects(pygame.key.name(self.control), self.smallFont, WHITE)
        self.controlRect.center = (self.pos[0], self.pos[1] + 40)

        self.color = DARK_RED
        self.border = DARKER_RED

        self.display = display
        self.button = button.Button(self.pos[0] - 25, self.pos[1] - 25, 50, 50, None, None, None, self.display)
        self.pressed = False

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.button.update()

        pygame.draw.rect(self.display, self.color, (self.pos[0] - 25, self.pos[1] - 25, 50, 50))
        pygame.draw.rect(self.display, self.border, (self.pos[0] - 25, self.pos[1] - 25, 50, 50), 5)
        self.display.blit(self.nameSurf, self.nameRect)
        self.display.blit(self.controlSurf, self.controlRect)

        if self.button.pressed or self.pressed:
            self.pressed = True
            for key in input_list:
                if pressed_keys[key]:
                    self.control = key
                    self.controlSurf, self.controlRect = text_objects(pygame.key.name(self.control),
                                                                      self.smallFont, WHITE)
                    self.controlRect.center = (self.pos[0], self.pos[1] + 40)
                    self.pressed = False

        if self.button.pressed or self.pressed:
            self.color = BLUE
            self.border = DARK_BLUE
        else:
            self.color = DARK_RED
            self.border = DARKER_RED


class controlPanel:
    def __init__(self, display, controls=(K_LEFT, K_RIGHT, K_UP, K_DOWN, K_h), pos=(WIDTH/2, HEIGHT/2)):
        self.controls = controls
        self.pos = pos
        self.display = display
        self.left = controlButton("<", self.controls[0], (self.pos[0] - 60, self.pos[1] + 50), self.display)
        self.right = controlButton(">", self.controls[1], (self.pos[0] + 60, self.pos[1] + 50), self.display)
        self.up = controlButton("^", self.controls[2], (self.pos[0], self.pos[1] - 50), self.display)
        self.down = controlButton("v", self.controls[3], (self.pos[0], self.pos[1] + 50), self.display)
        self.attack = controlButton("Atk", self.controls[4], (self.pos[0] + 60, self.pos[1] - 50), self.display, bigSize=30)

    def update(self):
        self.left.update()
        self.right.update()
        self.down.update()
        self.up.update()
        self.attack.update()

    def reInit(self, controls):
        self.controls = controls
        self.left = controlButton("<", self.controls[0], (self.pos[0] - 60, self.pos[1] + 50), self.display)
        self.right = controlButton(">", self.controls[1], (self.pos[0] + 60, self.pos[1] + 50), self.display)
        self.up = controlButton("^", self.controls[2], (self.pos[0], self.pos[1] - 50), self.display)
        self.down = controlButton("v", self.controls[3], (self.pos[0], self.pos[1] + 50), self.display)
        self.attack = controlButton("Atk", self.controls[4], (self.pos[0] + 60, self.pos[1] - 50), self.display, bigSize=30)

    def returnControls(self):
        return [self.left.control, self.right.control, self.up.control, self.down.control, self.attack.control]
