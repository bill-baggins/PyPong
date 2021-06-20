import pygame
import json
import os.path

from sys import exit

from pong.game import pong_loop
from pong.menu import menu_loop
from pong.common import MenuState
from pong.options import OPTION


# The main loop. Contains some pygame boilerplate and also contains two loops:
# the menu loop and the game loop.

def main_loop(width, height, title, fullscreen=False, fps: int = 60):
    available_resolutions = pygame.display.list_modes()
    clock = pygame.time.Clock()
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    size = width, height
    if fullscreen and size not in available_resolutions:
        raise Exception("That resolution is not supported by your monitor.")

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN if fullscreen else 0)
    pygame.display.set_caption(title)

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    menu_state = MenuState.Menu

    # Joystick support is still not done. Need to provide functionality for navigating
    # the menu using a controller.
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    # Main game loop goes here. Will switch between the menu and the game.
    while menu_state != MenuState.Quit:
        if menu_state == MenuState.Menu:
            menu_state = menu_loop(screen, screen_width, screen_height, font, clock, fps)
        elif menu_state == MenuState.Game:
            menu_state = pong_loop(screen, screen_width, screen_height, font, clock, fps, joysticks=joysticks)


if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()
    pygame.font.init()

    main_loop(768, 432, "Pong", False, 60)

    with open("options.json", "w+") as f:
        json.dump(OPTION, f)

    pygame.font.quit()
    pygame.quit()
    exit()
