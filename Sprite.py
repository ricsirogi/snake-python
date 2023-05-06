import pygame
import time
from collections import deque
import math


class Snake_head(object):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: list[int], time_between_movements: float, screen: pygame.surface.Surface, unit: tuple[int, int], map: tuple[int, int], eye_color: list[int], map_x_offset: int, map_y_offset: int):
        self.rect = pygame.rect.Rect(pos, size)
        self.size = size
        self.color = color
        self.eye_color = eye_color
        self.surface = screen
        self.direction = ""
        self.time_between_movements = time_between_movements
        self.last_movement = 0
        self.last_follow = 0
        self.unit = unit
        self.map = map
        self.map_x_offset = map_x_offset
        self.map_y_offset = map_y_offset
        self.behind = None

        self.before_direction = ""
        self.input_queue = deque()
        self.max_queue_len = 2
        self.up_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.DIRECTIONS = ["u", "r", "d", "l"]
        self.collided_with_border = False
        self.eyes = [pygame.rect.Rect(pos, (int(
            size[0]/3), int(size[1]/3))), pygame.rect.Rect(pos, (int(size[0]/3), int(size[1]/3)))]

    def eyes_update(self, specific_direction=None):
        if specific_direction is not None:
            direction = specific_direction
        else:
            direction = self.direction

        if direction == "u":
            self.eyes[0].left = self.rect.left + int(self.size[0] / 9)
            self.eyes[0].top = self.rect.top + int(self.size[0] / 9)
            self.eyes[1].left = self.rect.left + 6 * int(self.size[0] / 9)
            self.eyes[1].top = self.rect.top + int(self.size[0] / 9)
        if direction == "r":
            self.eyes[0].left = self.rect.left + 6 * int(self.size[0] / 9)
            self.eyes[0].top = self.rect.top + int(self.size[0] / 9)
            self.eyes[1].left = self.rect.left + 6 * int(self.size[0] / 9)
            self.eyes[1].top = self.rect.top + 6 * int(self.size[0] / 9)
        if direction == "d":
            self.eyes[0].left = self.rect.left + int(self.size[0] / 9)
            self.eyes[0].top = self.rect.top + 6 * int(self.size[0] / 9)
            self.eyes[1].left = self.rect.left + 6 * int(self.size[0] / 9)
            self.eyes[1].top = self.rect.top + 6 * int(self.size[0] / 9)
        if direction == "l":
            self.eyes[0].left = self.rect.left + int(self.size[0] / 9)
            self.eyes[0].top = self.rect.top + int(self.size[0] / 9)
            self.eyes[1].left = self.rect.left + int(self.size[0] / 9)
            self.eyes[1].top = self.rect.top + 6 * int(self.size[0] / 9)

    def get_keyboard(self):
        keyboard = pygame.key.get_pressed()
        queue_len = len(self.input_queue)

        # these check if the input is a duplicate, if not, adds the input to the input queue
        if keyboard[pygame.K_UP]:
            if not self.up_pressed:
                self.up_pressed = True
                if queue_len != 0:
                    if "u" != self.input_queue[queue_len - 1] and queue_len < self.max_queue_len:
                        self.input_queue.append("u")
                else:
                    self.input_queue.append("u")
        else:
            self.up_pressed = False
        queue_len = len(self.input_queue)

        if keyboard[pygame.K_RIGHT]:
            if not self.right_pressed:
                self.right_pressed = True
                if queue_len != 0:
                    if "r" != self.input_queue[queue_len - 1] and queue_len < self.max_queue_len:
                        self.input_queue.append("r")
                else:
                    self.input_queue.append("r")
        else:
            self.right_pressed = False

        queue_len = len(self.input_queue)

        if keyboard[pygame.K_DOWN]:
            if not self.down_pressed:
                self.down_pressed = True
                if queue_len != 0:
                    if "d" != self.input_queue[queue_len - 1] and queue_len < self.max_queue_len:
                        self.input_queue.append("d")
                else:
                    self.input_queue.append("d")
        else:
            self.down_pressed = False

        queue_len = len(self.input_queue)

        if keyboard[pygame.K_LEFT]:
            if not self.left_pressed:
                self.left_pressed = True
                if queue_len != 0:
                    if "l" != self.input_queue[queue_len - 1] and queue_len < self.max_queue_len:
                        self.input_queue.append("l")
                else:
                    self.input_queue.append("l")
        else:
            self.left_pressed = False

        if len(self.input_queue) != 0:
            if not self.check_valid_movement(self.input_queue[0]):
                self.input_queue.popleft()

    def check_valid_movement(self, movement: str) -> bool:
        """
        checks if the upcoming move in the input queue is trying to go to the opposite of the current direction\n
        returns if the move is valid or not
        """
        if self.DIRECTIONS.index(movement) <= 1:
            if self.DIRECTIONS[self.DIRECTIONS.index(movement) + 2] == self.direction:
                return False
            else:
                return True
        else:
            if self.DIRECTIONS[self.DIRECTIONS.index(movement) - 2] == self.direction:
                return False
            else:
                return True

    def move(self, direction=None):
        self.get_keyboard()

        if time.time() - self.time_between_movements >= self.last_movement or direction is not None:
            self.before_direction = self.direction

            if len(self.input_queue) != 0:
                self.direction = self.input_queue.popleft()

            if self.direction != self.before_direction:
                print(f"Snake_head new direction: {self.direction}")

            if direction is not None:
                self.direction = direction

            pos = [self.rect.left, self.rect.top]
            if self.direction == "u":
                pos[1] -= self.unit[1]
            elif self.direction == "r":
                pos[0] += self.unit[0]
            elif self.direction == "d":
                pos[1] += self.unit[1]
            elif self.direction == "l":
                pos[0] -= self.unit[0]

            # if this new movement puts the snake to a position that is still inside the map, move it
            if self.map_x_offset < pos[0] < self.map[0] and self.map_y_offset < pos[1] < self.map[1]:
                self.rect.left = pos[0]
                self.rect.top = pos[1]
                self.last_movement = time.time()

                # If I'm not the last one and I wasn't given a specific direction, move the body part behind me
                if self.behind is not None and direction is None:
                    self.behind.move()
                self.eyes_update()

            else:
                self.collided_with_border = True
                self.eyes_update()

    def draw(self):
        pygame.draw.rect(self.surface, self.color,
                         self.rect)
        if self.direction == "":
            self.eyes_update("u")
        for i in self.eyes:
            pygame.draw.rect(self.surface, self.eye_color, i)


class Snake_body():
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: list[int], screen: pygame.surface.Surface, ahead, unit: tuple[int, int], map: tuple[int, int], behind=None):
        self.rect = pygame.rect.Rect(pos, size)
        self.size = size
        self.color = color
        self.surface = screen
        self.direction = ""
        self.ahead = ahead
        self.behind = behind
        self.unit = unit
        self.map = map
        self.time_between_movements = self.ahead.time_between_movements
        self.last_movement = 0

    def move(self):
        self.before_direction = self.direction
        self.direction = self.ahead.before_direction

        pos = [self.rect.left, self.rect.top]
        if self.direction == "u":
            pos[1] -= self.unit[1]
        elif self.direction == "r":
            pos[0] += self.unit[0]
        elif self.direction == "d":
            pos[1] += self.unit[1]
        elif self.direction == "l":
            pos[0] -= self.unit[0]

        self.rect.left = pos[0]
        self.rect.top = pos[1]
        self.last_movement = time.time()
        if self.behind is not None and (self.behind.rect.x, self.behind.rect.y) != (self.rect.x, self.rect.y):
            self.behind.move()

    def draw(self):
        pygame.draw.rect(self.surface, self.color,
                         self.rect)
