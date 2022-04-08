# TODO:
#       1) Add a navigation box to the main menu that can be controlled using the controller
#       or keyboard.
#       2) Improve the code structure for fonts. Make each Textbox and Button class work with their
#       own font objects

def main_loop(width: int, height: int, title: str, fullscreen: bool = False, fps: int = 60):
    available_resolutions = pygame.display.list_modes()
    clock = pygame.time.Clock()
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
            menu_state = menu_loop(screen, screen_width, screen_height)
        elif menu_state == MenuState.Game:
            menu_state = pong_loop(screen, screen_width, screen_height, clock, fps, joysticks=joysticks)


if __name__ == "__main__":
    import pygame
    import json
    import os.path

    pygame.init()

    from sys import exit

    from pong.game import pong_loop
    from pong.menu import menu_loop
    from pong.myenums import MenuState
    from pong.options import OPTION

    # The main loop. Contains some pygame boilerplate and also contains two loops:
    # the menu loop and the game loop.

    main_loop(800, 450, "Pong", False, 75)

    with open(os.path.basename("options.json"), "w+") as f:
        json.dump(OPTION, f)

    pygame.quit()
    exit()
