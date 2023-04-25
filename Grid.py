import pygame
import math
import numpy as np


class Grid(object):
    def __init__(self, pos: tuple[int, int], row_column: list[int], cell_size: list[int], cell_color: list[int], border_color: list[int], border_size: int, screen: pygame.Surface):
        self.row_column = row_column
        self.cell_size = cell_size
        self.cell_color = cell_color
        self.border_color = border_color
        self.border_size = border_size
        self.pos = pos
        self.x_positions = []
        self.y_positions = []
        self.all_positions = []
        self.cells = []
        self.screen = screen
        self.ships = {}
        self.hits = {}
        self.locked_ships = {}
        self.returned_value = None
        self.was_clicked = False

        border_width = self.cell_size[0] * self.row_column[0] + \
            (self.row_column[0] + 1) * self.border_size
        border_height = self.cell_size[1] * self.row_column[1] + \
            (self.row_column[1] + 1) * self.border_size

        self.border = pygame.Rect(
            (self.pos), (border_width, border_height))

        for i in range(self.row_column[1]):
            self.cells.append([])
            pos_y = self.pos[1] + self.cell_size[1] * i + \
                self.border_size * i + self.border_size
            if pos_y not in self.y_positions:
                self.y_positions.append(pos_y)

            for j in range(self.row_column[0]):
                pos_x = self.pos[0] + self.cell_size[0] * j + \
                    self.border_size * j + self.border_size
                if pos_x not in self.x_positions:
                    self.x_positions.append(pos_x)
                self.cells[i].append(pygame.Rect(
                    (pos_x, pos_y), self.cell_size))

        for y in range(self.row_column[1]):
            self.all_positions.append([])
            for x in range(self.row_column[0]):
                self.all_positions[y].append(
                    (self.x_positions[x], self.y_positions[y]))

    def get_all_positions(self) -> list[list[tuple[int, int]]]:
        return self.all_positions

    def remove_from_grid(self, ship_num):
        self.locked_ships.pop(str(ship_num))

    def real_round(self, number: float) -> int:
        """
        scuffed rounding
        """

        if number == int(number):
            return int(number)
        # print("checking the number:", number, "->", str(number/10)[3])
        if int(str(number/10)[3]) < 6:
            return int(number)
        else:
            return int(number) + 1

    def draw(self):
        pygame.draw.rect(self.screen, self.border_color, self.border)
        for y in self.cells:
            for x in y:
                pygame.draw.rect(self.screen, self.cell_color, x)

    def __del__(self):
        pass
