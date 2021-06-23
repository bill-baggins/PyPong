from typing import Union, Callable

import pygame
from pygame.constants import *

from .common import Color
from .common import MenuState, TextBox


class Button(TextBox):
    """
    This is my Button class. It is another GUI object that inherits from the
    TextBox class. The button class contains all the same attributes as the
    TextBox class, but with one added function: on_click. When clicked, it return
    the menu_state the button was intended to change.
    """
    def __init__(self, 
                 pos: list,
                 size: list,
                 background_color: list,
                 action: object,
                 text: str = "",
                 text_size: int = 20,
                 text_pos: list = None,
                 text_color: tuple = Color.Black):

        super().__init__(pos, size, background_color, text, text_pos, text_size, text_color)
        self.action = action

    # IMPORTANT: this function changes the MenuState. Gotta put this here
    # so i don't confuse myself later if something breaks because of this.
    def on_click(self, mouse_pos: tuple) -> Union[Callable, object]:
        if (self.rect.left < mouse_pos[0] < self.rect.right and
                self.rect.top < mouse_pos[1] < self.rect.bottom):
            return self.action


def menu_loop(screen: pygame.Surface,
              screen_width: int,
              screen_height: int) -> MenuState:

    # import OPTION here so it is not undefined
    from .options import OPTION

    # MAIN MENU BUTTONS -----------------------------------------------------------------------------------------------
    title_box = TextBox([screen_width // 2 - 100, 10],
                        [200, 50],
                        OPTION["BACKGROUND_COLOR"],
                        text="Pong!",
                        text_size=50,
                        text_color=Color.White)

    start_game = MenuState.Game
    open_options_menu = MenuState.Options
    quit_game = MenuState.Quit

    start_button = Button([screen_width // 2 - 100, title_box.size[1] * 2 + 30],
                          [200, 50],
                          Color.White,
                          action=start_game,
                          text="Start Game",
                          text_size=30)

    options_button = Button([screen_width // 2 - 100, title_box.size[1] * 4 + 30],
                            [200, 50],
                            Color.White,
                            action=open_options_menu,
                            text="Options",
                            text_size=30)

    quit_button = Button([screen_width // 2 - 100, title_box.size[1] * 6 + 30],
                         [200, 50],
                         Color.White,
                         action=quit_game,
                         text="Quit",
                         text_size=30)

    # END MAIN MENU BUTTONS -------------------------------------------------------------------------------------------

    # OPTION MENU TEXTBOX(ES) -----------------------------------------------------------------------------------------
    winning_score_str = f"Max Score:{OPTION['WINNING_SCORE']}"
    current_winning_score_text_box = TextBox([screen_width // 2 - 100, title_box.size[1] * 4 + 30], 
                                             [200, 50],
                                             Color.White, 
                                             text=winning_score_str, 
                                             text_size=30)

    # END OPTION MENU TEXT BOXES --------------------------------------------------------------------------------------

    # OPTION MENU BUTTON ACTIONS AND BUTTONS --------------------------------------------------------------------------
    return_to_main_menu = MenuState.Menu

    def update_winning_score_str():
        new_score_str = f"Max Score:{OPTION['WINNING_SCORE']}"
        current_winning_score_text_box.text = new_score_str
        current_winning_score_text_box.text_render = \
                current_winning_score_text_box.font.render(new_score_str, False, Color.Black)
        current_winning_score_text_box.update_text()

    def increase_winning_score():
        if OPTION["WINNING_SCORE"] < 15:
            OPTION["WINNING_SCORE"] += 1
            update_winning_score_str()

    def decrease_winning_score():
        if OPTION["WINNING_SCORE"] > 1:
            OPTION["WINNING_SCORE"] -= 1
            update_winning_score_str()

    increase_score_button = Button([screen_width // 2 + 120, title_box.size[1] * 4 + 30],
                                   [40, 50],
                                   Color.White,
                                   action=increase_winning_score,
                                   text=">",
                                   text_size=80)

    decrease_score_button = Button([screen_width // 2 - 160, title_box.size[1] * 4 + 30],
                                   [40, 50],
                                   Color.White,
                                   action=decrease_winning_score,
                                   text="<",
                                   text_size=80)

    back_to_main_menu_button = Button([screen_width // 2 - 100, title_box.size[1] * 6 + 30],
                                      [200, 50],
                                      Color.White,
                                      action=return_to_main_menu,
                                      text="Main Menu",
                                      text_size=30)

    # END OPTION MENU BUTTONS -----------------------------------------------------------------------------------------

    main_menu_buttons = start_button, options_button, quit_button
    option_menu_buttons = increase_score_button, decrease_score_button, back_to_main_menu_button,
    option_menu_text_boxes = current_winning_score_text_box,

    menu_state = MenuState.Menu

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONDOWN:
                # Loops through the main_menu buttons and checks to see if the
                # menu state has changed.
                if menu_state == MenuState.Menu:
                    for button in main_menu_buttons:
                        if button.on_click(mouse_pos) is not None:
                            menu_state = button.on_click(mouse_pos)

                elif menu_state == MenuState.Options:
                    for button in option_menu_buttons:
                        if button.on_click(mouse_pos) is not None:
                            button_action = button.on_click(mouse_pos)
                            if button_action in MenuState.val_range:
                                menu_state = button_action
                            else:
                                button_action()

        screen.fill(OPTION["BACKGROUND_COLOR"])

        title_box.draw_to(screen)

        if menu_state == MenuState.Menu:
            for button in main_menu_buttons:
                button.draw_to(screen)
        elif menu_state == MenuState.Game:
            running = False
            break
        elif menu_state == MenuState.Options:
            for textbox in option_menu_text_boxes:
                textbox.draw_to(screen)

            for button in option_menu_buttons:
                button.draw_to(screen)
        elif menu_state == MenuState.Quit:
            running = False
            break

        pygame.display.update()

    return menu_state
