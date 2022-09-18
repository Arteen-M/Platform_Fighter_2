import pygame


class Shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((0, 0))
        self.rect = self.surf.get_rect(midbottom=(0, 0))
        self.direction = None

    def update(self, shield_size, rect_pos, shield_direction):
        self.surf = pygame.Surface(shield_size)
        self.rect = self.surf.get_rect(midbottom=rect_pos)
        self.direction = shield_direction
