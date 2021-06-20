import pygame
from pygame.math import Vector2
from pygame.constants import *

from common import Color, XboxButton


class Paddle(object):
    def __init__(self,
                 pos: Vector2,
                 width: float,
                 height: float,
                 color: tuple,
                 valid_movement_keys: list = None,
                 joystick: pygame.joystick.Joystick = None):
        self.score = 0
        self.speed = 80
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color or (0, 0, 0)
        self.valid_movement_inputs = valid_movement_keys or []

        if joystick is not None:
            self.joystick = joystick

        self.surf = pygame.Surface([width, height])
        self.rect = self.surf.get_rect(topleft=pos)

        self.movement_key_dict = {}
        self.current_key = 0

    def draw_to(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, dt: float, screen_height: int):
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

        self.rect.y += self.movement_key_dict.get(self.current_key, 0) * dt
