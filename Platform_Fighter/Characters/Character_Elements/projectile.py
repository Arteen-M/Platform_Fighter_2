import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, size, pos, path, total_frames, display, set_speed=10):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface(size)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.surf.get_rect(midbottom=(self.pos_x, self.pos_y - 10))
        self.image_rect = self.image.get_rect(midbottom=(self.pos_x, self.pos_y))
        self.speed = set_speed
        self.frames = 0
        self.total_frames = total_frames
        self.display = display
        self.running = False

    def update(self):
        self.pos_x += self.speed
        self.rect = self.surf.get_rect(midbottom=(self.pos_x, self.pos_y - 10))
        self.image_rect = self.image.get_rect(midbottom=(self.pos_x, self.pos_y))
        self.frames += 1

        self.display.blit(self.surf, self.rect)
        self.display.blit(self.image, self.image_rect)

    def set(self, size, pos, total_frames):
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(midbottom=(self.pos_x, self.pos_y - 10))

        self.pos_x = pos[0]
        self.pos_y = pos[1]

        self.frames = 0
        self.total_frames = total_frames

        self.running = True

    def clear(self):
        self.surf = pygame.Surface((0, 0))
        self.pos_x = 0
        self.pos_y = 0
        self.running = False
