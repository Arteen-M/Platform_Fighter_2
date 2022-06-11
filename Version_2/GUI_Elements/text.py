import pygame

pygame.font.init()
font = 'impact'


class Text:
    def __init__(self, msg, font, size, color, pos, display):
        self.text = msg
        self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.pos = pos
        self.surf = self.font.render(self.text, True, self.color)
        self.rect = self.surf.get_rect(center=self.pos)
        self.display = display

    def draw(self):
        self.display.blit(self.surf, self.rect)

    def update(self, text=None, rect=None, color=None):
        if text is not None:
            self.text = text
        if color is not None:
            self.color = color
        if rect is not None:
            self.rect = self.surf.get_rect(center=rect)
        else:
            self.rect = self.surf.get_rect(center=self.pos)

        self.surf = self.font.render(self.text, True, self.color)

