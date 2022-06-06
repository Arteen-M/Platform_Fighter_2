import pygame

pygame.font.init()


class Text:
    def __init__(self, msg, font, size, color, pos, display):
        self.text = msg
        self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.surf = self.font.render(self.text, True, self.color)
        self.pos = pos
        self.rect = self.surf.get_rect(center=self.pos)
        self.display = display

    def draw(self):
        self.display.blit(self.surf, self.rect)

    def update(self, rect):
        self.rect = self.surf.get_rect(center=rect)

