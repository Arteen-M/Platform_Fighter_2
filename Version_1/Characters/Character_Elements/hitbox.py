import pygame
import time

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)


class HitBox(pygame.sprite.Sprite):
    def __init__(self, size, display, lag, start_flag, end_flag, direction, angle, damage, base, scale, hitstun, color=RED):
        super().__init__()
        self.surf = pygame.Surface(size)
        self.surf.set_alpha(100)
        self.rect = self.surf.get_rect(center=(0, 0))
        self.surf.fill(color)

        self._lag = lag
        self.start_flag = start_flag
        self.end_flag = end_flag

        self.count = self._lag
        self._active = False
        self.running = False

        self._direction = direction

        self.x_component = angle[0]
        self.y_component = angle[1]
        self.damage = damage
        self.base_knockback = base
        self.knockback_scale = scale
        self.hitstun = hitstun

        self.display = display

    @property
    def lag(self):
        return self._lag

    @property
    def active(self):
        return self._active

    def update(self, pos):
        self.running = True
        self.rect = self.surf.get_rect(center=pos)

        if self.count == self.start_flag:
            self._active = True
        if self.count == self.end_flag:
            self._active = False

        self.count -= 1

        if self.count <= 0:
            self.running = False
            self.count = self._lag

        if self._active:
            self.draw()

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    def draw(self):
        self.display.blit(self.surf, self.rect)

    def reset(self):
        self.count = self._lag
        self._active = False
        self.running = False