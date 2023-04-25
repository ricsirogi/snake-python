import pygame


class Apple():
    def __init__(self, color: list[int], size: tuple[int, int], screen: pygame.surface.Surface):
        self.rect = pygame.rect.Rect((0, 0), size)
        self.size = size
        self.color = color
        self.screen = screen

    def set_pos(self, pos):
        self.rect = pygame.rect.Rect(pos, self.size)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
