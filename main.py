import pygame
import Button
import Grid
import Sprite
import Apple
import sys
import random
import time


class Main():
    def __init__(self):
        pygame.init()

        self.GRID_POS = (0, 0)
        self.GRID_ROW_COLUMN = [30, 20]
        self.GRID_CELL_SIZE = [30, 30]
        self.GRID_CELL_COLOR = [0, 100, 50]
        self.GRID_BORDER_COLOR = [0, 150, 50]
        self.GRID_BORDER_SIZE = 1

        self.SNAKE_SIZE = (30, 30)
        self.SNAKE_COLOR = [0, 255, 0]
        self.SNAKE_HEAD_COLOR = [0, 180, 30]
        self.SNAKE_TIME_BETWEEN_MOVE = 0.12
        self.SAKE_STARTNG_BODY_SIZE = 2

        size_x = self.GRID_ROW_COLUMN[0] * self.GRID_CELL_SIZE[0] + \
            self.GRID_ROW_COLUMN[0] * \
            self.GRID_BORDER_SIZE + self.GRID_BORDER_SIZE
        size_y = self.GRID_ROW_COLUMN[1] * self.GRID_CELL_SIZE[1] + \
            self.GRID_ROW_COLUMN[1] * \
            self.GRID_BORDER_SIZE + self.GRID_BORDER_SIZE

        self.SIZE = (size_x, size_y)
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Python Snake")
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_started = False
        self.game_lost = False
        self.space_pressed = False

        self.grid = Grid.Grid(self.GRID_POS, self.GRID_ROW_COLUMN, self.GRID_CELL_SIZE,
                              self.GRID_CELL_COLOR, self.GRID_BORDER_COLOR, self.GRID_BORDER_SIZE, self.screen)

        self.all_positions = self.grid.all_positions

        self.SNAKE_HEAD_POS = self.all_positions[int(
            self.GRID_ROW_COLUMN[1] / 2)][int(self.GRID_ROW_COLUMN[0] / 2)]

        self.apple = Apple.Apple(
            [255, 0, 0], tuple(self.GRID_CELL_SIZE), self.screen)

    def snake_init(self):
        self.snake_head = Sprite.Sprite(
            self.clock, self.SNAKE_HEAD_POS, self.SNAKE_SIZE, self.SNAKE_HEAD_COLOR, self.SNAKE_TIME_BETWEEN_MOVE, True, self.screen, None)
        self.snake_body = []

        for i in range(self.SAKE_STARTNG_BODY_SIZE):
            if i == 0:
                ahead = self.snake_head
            else:
                ahead = self.snake_body[i - 1]
            self.snake_body.append(Sprite.Sprite(
                self.clock, self.SNAKE_HEAD_POS, self.SNAKE_SIZE, self.SNAKE_COLOR, self.SNAKE_TIME_BETWEEN_MOVE, False, self.screen, ahead))

        self.update_snake_body_positions()

        self.place_apple()

    def place_apple(self):
        possibe_places = self.all_positions
        while True:
            num_y = random.randint(0, len(possibe_places) - 1)
            num_x = random.randint(0, len(possibe_places[num_y]) - 1)
            random_pos = possibe_places[num_y][num_x]
            if random_pos not in self.snake_body_positions and random_pos != (self.apple.rect.x, self.apple.rect.y) and random_pos != (self.snake_head.rect.left, self.snake_head.rect.top):
                self.apple.set_pos(random_pos)
                break
            else:
                del random_pos

    def update_snake_body_positions(self):
        self.snake_body_positions = []
        for i in self.snake_body:
            self.snake_body_positions.append((i.rect.left, i.rect.top))

    def snake_stuff(self):
        if not self.game_lost:
            new_pos = self.get_new_snake_head_pos()
            snake_can_move = time.time() - \
                self.snake_head.time_between_movements >= self.snake_head.last_movement
            if new_pos != "game over" and snake_can_move:
                if new_pos == (self.apple.rect.x, self.apple.rect.y):
                    self.place_apple()
                    self.add_snake_body()
                self.snake_head.move(new_pos)
            else:
                if snake_can_move:
                    self.game_over()

        for i in self.snake_body:
            i.draw(self.game_lost)
        self.snake_head.draw()
        self.update_snake_body_positions()

    def add_snake_body(self):
        ahead = self.snake_body[len(self.snake_body) - 1]
        self.snake_body.append(Sprite.Sprite(
            self.clock, (ahead.rect.left, ahead.rect.top), self.SNAKE_SIZE, self.SNAKE_COLOR, self.SNAKE_TIME_BETWEEN_MOVE, False, self.screen, ahead))
        self.update_snake_body_positions()

    def get_new_snake_head_pos(self):
        move = self.snake_head.get_keyboard()
        new_pos = current_pos = (
            self.snake_head.rect.left, self.snake_head.rect.top)
        if move != "":
            if move == "u":
                current_pos = (self.snake_head.rect.left,
                               self.snake_head.rect.top)
                for y_count, y in enumerate(self.all_positions):
                    for x_count, x in enumerate(y):
                        if current_pos == x:
                            if y_count != 0:
                                new_pos = self.all_positions[y_count - 1][x_count]
                            else:
                                return "game over"
            elif move == "r":
                current_pos = (self.snake_head.rect.left,
                               self.snake_head.rect.top)
                for y_count, y in enumerate(self.all_positions):
                    for x_count, x in enumerate(y):
                        if current_pos == x:
                            if x_count != self.GRID_ROW_COLUMN[0] - 1:
                                new_pos = self.all_positions[y_count][x_count + 1]
                            else:
                                return "game over"
            elif move == "d":
                current_pos = (self.snake_head.rect.left,
                               self.snake_head.rect.top)
                for y_count, y in enumerate(self.all_positions):
                    for x_count, x in enumerate(y):
                        if current_pos == x:
                            if y_count != self.GRID_ROW_COLUMN[1] - 1:
                                new_pos = self.all_positions[y_count + 1][x_count]
                            else:
                                return "game over"
            elif move == "l":
                current_pos = (self.snake_head.rect.left,
                               self.snake_head.rect.top)
                for y_count, y in enumerate(self.all_positions):
                    for x_count, x in enumerate(y):
                        if current_pos == x:
                            if x_count != 0:
                                new_pos = self.all_positions[y_count][x_count - 1]
                            else:
                                return "game over"
        if new_pos in self.snake_body_positions and self.snake_head.direction != "":
            return "game over"
        return new_pos

    def button_click(self):
        self.snake_init()
        self.game_started = True
        self.game_lost = False

    def game_over(self):
        self.game_lost = True
        print("Game over :)")

    def mainloop(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if not self.space_pressed:
                    self.button_click()
                    self.space_pressed = True
            else:
                self.space_pressed = False
            if pygame.key.get_pressed()[pygame.K_d]:
                print("Debugging")

            self.screen.fill([50, 50, 50])

            self.grid.draw()

            if self.game_started:
                self.apple.draw()

            if self.game_started:
                self.snake_stuff()

            pygame.display.flip()
            self.clock.tick(75)


if __name__ == "__main__":
    app = Main()
    app.mainloop()
