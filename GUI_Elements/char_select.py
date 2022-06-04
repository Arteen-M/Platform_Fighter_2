import pygame


class charButton(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.surf = pygame.Surface((75, 100))
        self.pos = pos
        self.rect = self.surf.get_rect(center=self.pos)

