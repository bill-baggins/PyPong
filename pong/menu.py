import pygame

from pygame.constants import *

from .common import Color, TextBox, Button
from .myenums import MenuState


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
                                             text_size=25)

    # END OPTION MENU TEXT BOXES --------------------------------------------------------------------------------------

    # OPTION MENU BUTTON ACTIONS AND BUTTONS --------------------------------------------------------------------------
    return_to_main_menu = MenuState.Menu

    def update_winning_score_str() -> None:
        new_score_str = f"Max Score:{OPTION['WINNING_SCORE']}"
        current_winning_score_text_box.text = new_score_str
        current_winning_score_text_box.text_render = \
            current_winning_score_text_box.font.render(new_score_str, False, current_winning_score_text_box.text_color)
        current_winning_score_text_box.update_text()

    def increase_winning_score() -> None:
        if OPTION["WINNING_SCORE"] < 15:
            OPTION["WINNING_SCORE"] += 1
            update_winning_score_str()

    def decrease_winning_score() -> None:
        if OPTION["WINNING_SCORE"] > 1:
            OPTION["WINNING_SCORE"] -= 1
            update_winning_score_str()


    player_count_button = Button([screen_width // 2 - 100, title_box.size[1] * 2 + 30],
                                 [200, 50],
                                 Color.White,
                                 action=None,
                                 text=f"Players: {OPTION['PLAYER_COUNT']}",
                                 text_size=30)

    def change_player_count() -> None:
        if OPTION["PLAYER_COUNT"] == 1:
            OPTION["PLAYER_COUNT"] += 1
        else:
            OPTION["PLAYER_COUNT"] -= 1
        player_count_button.text = f"Players: {OPTION['PLAYER_COUNT']}"
        player_count_button.text_render = \
            player_count_button.font.render(player_count_button.text, False, player_count_button.text_color)
        player_count_button.update_text()

    player_count_button.action = change_player_count

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

    main_menu_buttons = (start_button,
                         options_button,
                         quit_button)

    option_menu_buttons = (player_count_button,
                           increase_score_button,
                           decrease_score_button,
                           back_to_main_menu_button,)

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
