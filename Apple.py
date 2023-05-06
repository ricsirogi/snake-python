import pygame


class Apple():
    def __init__(self, color: list[int], size: tuple[int, int], screen: pygame.surface.Surface):
        self.apple_pieces = []
        for i in range(4):
            apple_piece = pygame.rect.Rect((0, 0), (size[0]/3, size[1]/3))
            self.apple_pieces.append(apple_piece)

        self.size = size
        self.color = color
        self.screen = screen
        self.pos = (0, 0)

    def set_pos(self, pos):
        self.pos = pos

        # top piece
        self.apple_pieces[0].left = pos[0] + self.size[0]/3
        self.apple_pieces[0].top = pos[1]

        # right piece
        self.apple_pieces[1].left = pos[0] + self.size[0]/3 * 2
        self.apple_pieces[1].top = pos[1] + self.size[1]/3

        # bottom piece
        self.apple_pieces[2].left = pos[0] + self.size[0]/3
        self.apple_pieces[2].top = pos[1] + self.size[1]/3 * 2

        # left piece
        self.apple_pieces[3].left = pos[0]
        self.apple_pieces[3].top = pos[1] + self.size[1]/3

    def draw(self):
        for apple_piece in self.apple_pieces:
            pygame.draw.rect(self.screen, self.color, apple_piece)
