import pygame
import Button
import Grid
import Sprite
import Apple
import sys
import random
import time
import json


class Main():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.BUTTON_SIZE = [195, 80]
        self.BUTTON_ACOLOR = [155, 197, 200]
        self.BUTTON_IACOLOR = [155, 197, 100]
        self.BUTTON_TEXT = "START!"
        self.BUTTON_TEXT_COLOR = [255, 255, 255]
        self.BUTTON_TEXT_SIZE = 70

        self.GRID_ROW_COLUMN = [20, 20]
        self.GRID_CELL_SIZE = [30, 30]
        self.GRID_CELL_COLOR = [155, 197, 2]
        self.GRID_BORDER_COLOR = [155, 197, 2]
        self.GRID_BORDER_SIZE = 1

        self.GRAND_BORDER_THICKNESS = 10
        self.GRAND_BORDER_SIZE = (
            self.GRID_ROW_COLUMN[0] *
            (self.GRID_CELL_SIZE[0] + self.GRID_BORDER_SIZE),
            self.GRID_ROW_COLUMN[1] * (self.GRID_CELL_SIZE[1] + self.GRID_BORDER_SIZE))
        self.GRAND_BORDER_COLOR = [0, 0, 0]

        self.SCORE_DISPLAY_TEXT_COLOR = [0, 0, 0]
        self.SCORE_DISPLAY_TEXT_SIZE = int(self.GRID_CELL_SIZE[0] * 1.5)

        self.font = pygame.font.SysFont(
            "Consolas", self.SCORE_DISPLAY_TEXT_SIZE)
        self.score_display = self.font.render("Score: 0", True, [0, 0, 0])
        self.game_over_text = self.font.render("Game over", True, [0, 0, 0])
        self.high_score_text = self.font.render("High_score:", True, [0, 0, 0])
        self.UNIT_X = self.GRID_CELL_SIZE[0] + self.GRID_BORDER_SIZE
        self.UNIT_Y = self.GRID_CELL_SIZE[1] + self.GRID_BORDER_SIZE

        # Size of the whole map that the snake can move in
        self.MAP_X = self.UNIT_X * \
            self.GRID_ROW_COLUMN[0] + self.GRID_BORDER_SIZE
        self.MAP_Y = self.UNIT_Y * \
            self.GRID_ROW_COLUMN[1] + self.GRID_BORDER_SIZE

        self.SOCRE_BACKGROUND_SIZE = [
            self.MAP_X + self.GRAND_BORDER_THICKNESS * 2, self.SCORE_DISPLAY_TEXT_SIZE]

        self.SCORE_DISPLAY_POS = (self.SOCRE_BACKGROUND_SIZE[1], 0)

        self.GRID_POS = (self.GRAND_BORDER_THICKNESS + self.SOCRE_BACKGROUND_SIZE[1], self.GRAND_BORDER_THICKNESS +
                         self.SOCRE_BACKGROUND_SIZE[1])
        self.grand_border = pygame.rect.Rect((self.SOCRE_BACKGROUND_SIZE[1], self.SOCRE_BACKGROUND_SIZE[1]), (
            self.MAP_X + self.GRAND_BORDER_THICKNESS * 2, self.MAP_Y + self.GRAND_BORDER_THICKNESS * 2))

        self.SNAKE_SIZE = tuple(self.GRID_CELL_SIZE)
        self.SNAKE_COLOR = [0, 0, 0]
        self.SNAKE_HEAD_COLOR = [0, 0, 0]
        self.SNAKE_TIME_BETWEEN_MOVE = 0.1  # 0.1
        self.SAKE_STARTNG_BODY_SIZE = 2
        self.SNAKE_EYE_COLOR = [155, 197, 2]

        size_x = self.GRID_ROW_COLUMN[0] * (
            self.GRID_CELL_SIZE[0] + self.GRID_BORDER_SIZE) + self.GRID_BORDER_SIZE + self.GRAND_BORDER_THICKNESS * 2
        size_y = self.GRID_ROW_COLUMN[1] * (
            self.GRID_CELL_SIZE[1] + self.GRID_BORDER_SIZE) + self.GRID_BORDER_SIZE + self.GRAND_BORDER_THICKNESS * 2 + self.SOCRE_BACKGROUND_SIZE[1]

        # don't touch the next 4 lines they just work
        self.map_x_offset = int((size_x - self.MAP_X) * 2)
        self.MAP_X += self.map_x_offset

        self.map_y_offset = int((size_y - self.MAP_Y) / 2)
        self.MAP_Y += self.map_y_offset

        self.APPLE_STRENGTH = 1  # how many "body parts" each apple gives
        self.APPLE_COLOR = [0, 100, 0]

        self.screen = pygame.display.set_mode(
            (size_x + self.SOCRE_BACKGROUND_SIZE[1] * 2, size_y + self.SOCRE_BACKGROUND_SIZE[1]))
        pygame.display.set_caption("Python Snake")
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_started = False
        self.game_lost = False
        self.space_pressed = False
        self.score = 0
        self.paused = False
        self.game_over_sequence_completed = False

        self.grid = Grid.Grid(self.GRID_POS, self.GRID_ROW_COLUMN, self.GRID_CELL_SIZE,
                              self.GRID_CELL_COLOR, self.GRID_BORDER_COLOR, self.GRID_BORDER_SIZE, self.screen)

        self.all_positions = self.grid.all_positions

        self.SNAKE_HEAD_POS = self.all_positions[int(
            self.GRID_ROW_COLUMN[1] / 2)][int(self.GRID_ROW_COLUMN[0] / 2)]

        self.BUTTON_POS = (
            self.SNAKE_HEAD_POS[0] - self.BUTTON_SIZE[0] / 2, self.SNAKE_HEAD_POS[1] + self.SNAKE_HEAD_POS[1] / 4)

        self.button = Button.Button(
            self.BUTTON_TEXT, self.BUTTON_POS, tuple(self.BUTTON_SIZE), self.BUTTON_ACOLOR, self.BUTTON_IACOLOR, self.BUTTON_TEXT_COLOR, lambda: self.button_click(), self.screen, self.BUTTON_TEXT_SIZE)
        self.apple = Apple.Apple(
            self.APPLE_COLOR, tuple(self.GRID_CELL_SIZE), self.screen)

    def snake_init(self):
        "Generates the starting snake"

        # Generates the snake head and body parts
        self.snake_head = Sprite.Snake_head(
            self.SNAKE_HEAD_POS, self.SNAKE_SIZE, self.SNAKE_HEAD_COLOR, self.SNAKE_TIME_BETWEEN_MOVE, self.screen, (self.UNIT_X, self.UNIT_Y), (self.MAP_X, self.MAP_Y), self.SNAKE_EYE_COLOR, self.map_x_offset, self.map_y_offset)

        self.snake_body = []
        for i in range(self.SAKE_STARTNG_BODY_SIZE):
            if i == 0:
                ahead = self.snake_head
            else:
                ahead = self.snake_body[i - 1]
            body = Sprite.Snake_body(
                self.SNAKE_HEAD_POS, self.SNAKE_SIZE, self.SNAKE_COLOR, self.screen, ahead, (self.UNIT_X, self.UNIT_Y), (self.MAP_X, self.MAP_Y))
            self.snake_body.append(body)

        self.snake_head.behind = self.snake_body[0]
        # lets each body part (and the head) know who is behind them
        for c, i in enumerate(self.snake_body):
            if c < len(self.snake_body) - 1:
                i.behind = self.snake_body[c + 1]
        self.update_snake_body_positions()

        self.place_apple()

    def place_apple(self):
        possibe_places = self.all_positions
        while True:
            num_y = random.randint(0, len(possibe_places) - 1)
            num_x = random.randint(0, len(possibe_places[num_y]) - 1)
            random_pos = possibe_places[num_y][num_x]
            if random_pos not in self.snake_body_positions and random_pos != self.apple.pos and random_pos != (self.snake_head.rect.left, self.snake_head.rect.top):
                self.apple.set_pos(random_pos)
                break
            else:
                del random_pos

    def update_snake_body_positions(self):
        self.snake_body_positions = []
        for i in self.snake_body:
            self.snake_body_positions.append((i.rect.left, i.rect.top))

    def update_score(self, reset=False):
        if reset:
            self.score = 0
        else:
            self.score += 1 * self.APPLE_STRENGTH

        self.score_display = self.font.render(
            "Score: " + str(self.score), True, self.SCORE_DISPLAY_TEXT_COLOR)

    def snake_stuff(self):
        if not self.paused:
            # check if snake_head is on top of an apple
            if (self.snake_head.rect.left, self.snake_head.rect.top) == self.apple.pos:
                self.add_snake_body()
                self.place_apple()
                self.update_score()
            if not self.game_lost:
                self.snake_head.move()

            # checking for game over by colliding with itself
            if self.snake_head.before_direction != "" and not self.game_lost:
                for i in self.snake_body_positions:
                    if i == (self.snake_head.rect.x, self.snake_head.rect.y):
                        self.game_lost = True

                        # make the snake_head go back one unit and add a snake_body at the end, so it looks like it just stopped, but in reality I don't know how else I could imploment this
                        backwards_direction = ""
                        current_direction = self.snake_head.direction

                        if current_direction == "u":
                            backwards_direction = "d"
                        elif current_direction == "r":
                            backwards_direction = "l"
                        elif current_direction == "d":
                            backwards_direction = "u"
                        elif current_direction == "l":
                            backwards_direction = "r"

                        self.snake_head.move(backwards_direction)
                        self.snake_head.eyes_update(current_direction)
                        temp = self.APPLE_STRENGTH
                        self.APPLE_STRENGTH = 1
                        self.add_snake_body()
                        self.APPLE_STRENGTH = temp

            if self.snake_head.collided_with_border:
                self.game_over()

        for i in self.snake_body:
            i.draw()

        self.snake_head.draw()

        self.update_snake_body_positions()

    def add_snake_body(self):

        for i in range(self.APPLE_STRENGTH):
            ahead = self.snake_body[len(self.snake_body) - 1]
            body_pos = [ahead.rect.left, ahead.rect.top]

            if ahead.direction == "u":
                body_pos[1] += self.UNIT_Y
            if ahead.direction == "r":
                body_pos[0] -= self.UNIT_X
            if ahead.direction == "d":
                body_pos[1] -= self.UNIT_Y
            if ahead.direction == "l":
                body_pos[0] += self.UNIT_X
            else:
                pass

            body = Sprite.Snake_body(
                tuple(body_pos), self.SNAKE_SIZE, self.SNAKE_COLOR, self.screen, ahead, (self.UNIT_X, self.UNIT_Y), (self.MAP_X, self.MAP_Y))
            self.snake_body.append(body)

            self.snake_body[len(self.snake_body) - 2].behind = body
        self.update_snake_body_positions()

    def button_click(self):
        self.snake_init()
        self.update_score(reset=True)
        self.game_started = True
        self.game_lost = False
        self.game_over_sequence_completed = False

    def button_stuff(self):
        self.button.get_mouse()
        self.button.draw()

    def game_over(self):
        if not self.game_over_sequence_completed:
            self.game_lost = True
            with open('datajson.json', "r") as f:
                current_data = json.load(f)

            if current_data["high_score"] < self.score:
                current_data['high_score'] = self.score
                with open('datajson.json', 'w') as f:
                    json.dump(current_data, f)
            else:
                pass

            self.game_over_sequence_completed = True

    def game_over_text_display(self):
        pass

    def pause(self):
        if self.paused == True:
            self.paused = False
        else:
            self.paused = True

    def mainloop(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)

            if pygame.key.get_pressed()[pygame.K_x]:
                sys.exit(0)

            if not self.game_lost and self.game_started:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    if not self.space_pressed:
                        self.pause()
                        self.space_pressed = True
                else:
                    self.space_pressed = False

            if pygame.key.get_pressed()[pygame.K_d]:
                print("Debugging")

            self.screen.fill(self.GRID_CELL_COLOR)

            pygame.draw.rect(
                self.screen, self.GRAND_BORDER_COLOR, self.grand_border)

            self.grid.draw()

            if self.game_started:
                self.apple.draw()

            if self.game_started:
                self.snake_stuff()

            if not self.game_started or self.game_lost:
                self.button_stuff()

            if self.game_lost:
                self.game_over_text_display()

            self.screen.blit(self.score_display, self.SCORE_DISPLAY_POS)
            pygame.display.flip()
            self.clock.tick(75)


if __name__ == "__main__":
    app = Main()
    app.mainloop()
