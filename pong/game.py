import pygame
from sys import exit
from pygame.math import Vector2
from pygame.constants import *

from .common import Color, GameState, XboxButton, MenuState
from .ball import Ball
from .paddle import Player
from .net import create_net_texture, draw_net

from .options import OPTION


def pong_loop(screen: pygame.Surface,
              screen_width: int,
              screen_height: int,
              font: pygame.font.Font,
              clock: pygame.time.Clock,
              fps: int = 60,
              joysticks: list = None) -> MenuState:

    num_of_players = OPTION["NUM_OF_PLAYERS"]
    ms = 0

    if joysticks is None:
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    player_one = Player(Vector2(20, 20), 20.0, 60.0, OPTION["PLAYER1_COLOR"], [K_w, K_s])
    player_two = Player(Vector2(screen_width - 40, 20), 20.0, 60.0, OPTION["PLAYER2_COLOR"], [K_UP, K_DOWN])

    if num_of_players == 1:
        pass

    ball = Ball(10, screen_width, screen_height, 300, OPTION["BALL_COLOR"])
    net_texture = create_net_texture(5, screen_height)

    player_joystick_list = [player_one, player_two]

    for _, p in enumerate((player_one, player_two)):
        p.movement_key_dict[p.valid_movement_inputs[0]] = -180
        p.movement_key_dict[p.valid_movement_inputs[1]] = 240

    if len(joysticks) == num_of_players:
        for i, p in enumerate((player_one, player_two)):
            p.joystick = joysticks[i]
            p.valid_movement_inputs = [
                *p.valid_movement_inputs,
                XboxButton.LB,
                XboxButton.RB
            ]
            p.movement_key_dict[XboxButton.LB] = -180
            p.movement_key_dict[XboxButton.RB] = 240

    def render_player_score(player: str, player_score: int) -> pygame.Surface:
        return font.render(f"{player}{player_score}", False, Color.Black)

    def render_player_got_point(player_number: str) -> pygame.Surface:
        return font.render(f"Player {player_number} got the point!", False, Color.Black)

    def render_player_won(player_number: str) -> pygame.Surface:
        return font.render(f"Player {player_number} won the game!", False, Color.Black)

    player_one_score_text = render_player_score("", player_one.score)
    player_two_score_text = render_player_score("", player_two.score)
    player_one_got_point_text = render_player_got_point("One")
    player_two_got_point_text = render_player_got_point("Two")

    # TODO: alternate the responsibility of resuming the game between the players.
    paused_text = font.render("Press the Spacebar or the A button to begin!", False, Color.Black)

    game_state = GameState.Paused

    running = True
    while running:
        dt = ms / 1000.0
        
        # Get user input.
        # NOTE: Currently the window will close when the player hits the A button on their
        # Xbox Controller OR the spacebar on the keyboard. This happens since - when the while
        # loop is terminated - the pong_loop function will return MenuState.Menu. Inside of the
        # while loop of the main_loop function in main.py, the MenuState is checked to see which
        # of two functions to run: menu_loop and pong_loop. When it runs menu_loop, it will return
        # MenuState.Quit and causes the whole application to quit.
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == KEYDOWN:

                # Starts the game.
                if game_state == GameState.Paused and event.key == K_SPACE:
                    game_state = GameState.Start

                # Puts the game into a paused state after the player got a point.
                if game_state == GameState.PlayerGotPoint and event.key == K_SPACE:
                    ball = Ball(10, screen_width, screen_height, 300, OPTION["BALL_COLOR"])
                    game_state = GameState.Paused

                # Quits back to the main menu
                if game_state == GameState.GameOver and event.key == K_SPACE:
                    running = False
                    break

                if event.key in player_one.valid_movement_inputs:
                    player_one.current_key = event.key

                if event.key in player_two.valid_movement_inputs:
                    player_two.current_key = event.key

            if event.type == KEYUP:
                if event.key in player_one.valid_movement_inputs:
                    player_one.current_key = 0

                if event.key in player_two.valid_movement_inputs:
                    player_two.current_key = 0

            # Similar to key-down events. Only real difference is that I need to get the ID
            # of the joystick before doing something with the input.
            if event.type == JOYBUTTONDOWN:
                for p in player_joystick_list:
                    if event.instance_id == p.joystick.get_instance_id() and \
                            event.button in p.valid_movement_inputs:
                        p.current_key = event.button

                # Resumes the Game. This happens after the player gets a point.
                if game_state == GameState.Paused and \
                        event.button == XboxButton.A:
                    game_state = GameState.Start

                # Pauses the game when the player gets a point.
                if game_state == GameState.PlayerGotPoint and \
                        event.button == XboxButton.A:
                    ball = Ball(10, screen_width, screen_height, 300, OPTION["BALL_COLOR"])
                    game_state = GameState.Paused

                # Quits out of the game. This happens when the game is over.
                if game_state == GameState.GameOver and \
                        event.button == XboxButton.A:
                    running = False
                    break

            if event.type == JOYBUTTONUP:
                for p in player_joystick_list:
                    if event.instance_id == p.joystick.get_instance_id() and \
                            event.button in p.valid_movement_inputs:
                        p.current_key = 0

        # Update objects.
        player_one.update(dt, screen_height)
        player_two.update(dt, screen_height)

        # Very rough code here. Basically determines who wins. Need to extract this to
        # either the paddle class or the ball class.
        if game_state == GameState.Start:
            ball.check_collision_with_player(player_one)
            ball.check_collision_with_player(player_two)
            ball.update(dt, screen_width, screen_height)

            if ball.exited_left_border or ball.exited_right_border:
                game_state = GameState.PlayerGotPoint
                if ball.exited_right_border:
                    player_one.score += 1
                    player_one_score_text = render_player_score("", player_one.score)
                    if player_one.score == OPTION["WINNING_SCORE"]:
                        game_state = GameState.GameOver
                        player_one_got_point_text = render_player_won("One")

                elif ball.exited_left_border:
                    player_two.score += 1
                    player_two_score_text = render_player_score("", player_two.score)
                    if player_two.score == OPTION["WINNING_SCORE"]:
                        game_state = GameState.GameOver
                        player_two_got_point_text = render_player_won("Two")

        # Draw to the screen.
        screen.fill(OPTION["BACKGROUND_COLOR"])

        # Draws the net as close to the center of the screen as possible.
        draw_net(screen, net_texture, (screen_width // 2) + net_texture.get_width() // 2, 0)

        if game_state == GameState.Paused:
            screen.blit(paused_text, [screen_width // 2 - paused_text.get_width() // 2,
                                      screen_height // 2 - 40])

        # Draw the player's score to the screen.
        screen.blit(player_one_score_text, [screen_width // 2 - 28, 20])
        screen.blit(player_two_score_text, [screen_width // 2 + 25, 20])

        # Draw the players to the screen.
        player_one.draw_to(screen)
        player_two.draw_to(screen)

        # Draw the ball to the screen.
        ball.draw_to(screen)

        # Display the "player got point" or winning text for each player.
        if ball.exited_right_border:
            screen.blit(player_one_got_point_text, [(screen_width / 2) - 100, screen_height / 2])
        elif ball.exited_left_border:
            screen.blit(player_two_got_point_text, [(screen_width / 2) - 100, screen_height / 2])

        # Tick the clock at the set framerate.
        ms = clock.tick(fps)

        # Update the display
        pygame.display.update()

    if not running:
        return MenuState.Menu

# WIP: Handling controller disconnect events.
# joystick_disconnected_text = font.render("A controller got disconnected. Please reconnect it.",
#                                          False,
#                                          Color.Black)
# if game_state == GameState.JoystickDisconnected:
# screen.blit(joystick_disconnected_text, [screen_width // 2 - joystick_disconnected_text.get_width() // 2,
#                                              screen_height // 2])
