import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, img, num_frames=4, multiplier=4, display=None):
        super().__init__()
        self.img_list = [img + str(x) + ".png" for x in range(0, num_frames)]
        self.surf = pygame.transform.scale(pygame.image.load(self.img_list[0]), (800, 600))
        self.rect = self.surf.get_rect(center=(400, 300))
        self.count = 0
        self.frame_count = 0
        self.multiplier = multiplier
        self.display = display

    def update(self):
        self.surf = pygame.transform.scale(pygame.image.load(self.img_list[self.count]), (800, 600))
        if self.frame_count % self.multiplier == 0:
            self.count += 1
        if self.count >= len(self.img_list):
            self.count = 0

        self.frame_count += 1

        self.display.blit(self.surf, self.rect)
