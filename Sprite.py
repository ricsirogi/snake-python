import pygame
import time
from collections import deque


class Sprite(object):
    def __init__(self, clock: pygame.time.Clock, pos: tuple[int, int], size: tuple[int, int], color: list[int], time_between_movements: float, is_head: bool, screen: pygame.surface.Surface, ahead):
        self.rect = pygame.rect.Rect(pos, size)
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.clock = clock
        self.color = color
        self.surface = screen
        self.direction = ""
        self.time_between_movements = time_between_movements
        self.last_movement = 0
        self.last_follow = 0
        self.is_head = is_head
        self.ahead = ahead
        self.before_pos = ()
        self.input_queue = deque()
        self.max_queue_len = 2
        self.up_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.DIRECTIONS = ["u", "r", "d", "l"]

    def get_keyboard(self):
        keyboard = pygame.key.get_pressed()
        temp = self.direction
        queue_len = len(self.input_queue)
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

        queue_len = len(self.input_queue)

        if queue_len != 0 and self.check_valid_movement():
            self.direction = self.input_queue[0]
        if temp != self.direction:
            print(self.direction)
        return self.direction

    def check_valid_movement(self):
        if self.DIRECTIONS.index(self.input_queue[0]) <= 1:
            if self.DIRECTIONS[self.DIRECTIONS.index(self.input_queue[0]) + 2] == self.direction:
                return False
            else:
                return True
        else:
            if self.DIRECTIONS[self.DIRECTIONS.index(self.input_queue[0]) - 2] == self.direction:
                return False
            else:
                return True

    # Imma make drastic changes to this shit so imma post this first
    def move(self, pos):
        if time.time() - self.time_between_movements >= self.last_movement:
            if len(self.input_queue) != 0:
                self.input_queue.popleft()
            self.before_pos = (self.rect.left, self.rect.top)
            self.rect.left = pos[0]
            self.rect.top = pos[1]
            self.rect = pygame.rect.Rect(pos, self.size)
            self.last_movement = time.time()

    def die(self):
        print("death")

    def draw(self, game_lost: bool = False):
        if not self.is_head and not game_lost:
            ahead_pos = (self.ahead.rect.left, self.ahead.rect.top)
            if abs(ahead_pos[0] - self.rect.left) > self.size[0] + 10 or abs(ahead_pos[1] - self.rect.top) > self.size[1]:
                self.move(self.ahead.before_pos)
        pygame.draw.rect(self.surface, self.color,
                         self.rect)
