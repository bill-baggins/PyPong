import pygame
from pygame.math import Vector2

from .paddle import Paddle

from random import randint, random


class Ball(object):
    def __init__(self, ball_radius: int, screen_width: int, screen_height: int, speed_x: int, color: tuple):
        self.pos = Vector2(screen_width / 2, screen_height / 2)
        self.speed_x = speed_x
        if round(random()) == 1:
            self.speed_x *= - 1

        self.speed_y = randint(-5, 5) * 10
        self.color = color or (0, 0, 0)
        self.exited_left_border = False
        self.exited_right_border = False

        self.surf = pygame.Surface([ball_radius, ball_radius])
        self.rect = self.surf.get_rect(topleft=self.pos)

    def draw_to(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, dt: float, screen_width: int, screen_height: int):
        self._check_collision_with_border(screen_width, screen_height)
        self.rect.x += self.speed_x * dt
        self.rect.y += self.speed_y * dt

    def check_collision_with_player(self, player: Paddle):
        if self.rect.colliderect(player.rect):
            self.rect.x = player.rect.left - self.rect.width if self.speed_x > 0 else player.rect.right
            if self.speed_x < 0:
                self.speed_x = -self.speed_x + 10
            else:
                self.speed_x = -(self.speed_x + 10)

            new_speed_y = randint(2, 5) * 30

            if round(random()) == 1:
                new_speed_y *= -1
            self.speed_y = new_speed_y

    def _check_collision_with_border(self, screen_width: int, screen_height: int):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = -self.speed_y
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.speed_y = -self.speed_y * 1.2

        if self.rect.x < -10:
            self.exited_left_border = True
        elif self.rect.x + self.rect.width - 10 > screen_width:
            self.exited_right_border = True
