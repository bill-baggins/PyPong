import pygame
from sys import exit
from pygame.math import Vector2
from pygame.constants import *

from .myenums import GameState, XboxButton, MenuState
from .common import Color, GameFont
from .ball import Ball
from .paddle import Player
from .net import create_net_texture, draw_net

from .options import OPTION


def pong_loop(screen: pygame.Surface,
              screen_width: int,
              screen_height: int,
              clock: pygame.time.Clock,
              fps: int = 60,
              joysticks: list = None) -> MenuState:

    player_count = OPTION["PLAYER_COUNT"]
    ms = 0

    player_one = Player(Vector2(20, 20), 20.0, 60.0, OPTION["PLAYER1_COLOR"], [K_w, K_s])
    player_two = Player(Vector2(screen_width - 40, 20), 20.0, 60.0, OPTION["PLAYER2_COLOR"], [K_UP, K_DOWN])

    if len(joysticks) != 0:
        if len(joysticks) == player_count:
            player_one.joystick = joysticks[0]
            player_two.joystick = joysticks[1]
        else:
            player_one.joystick = joysticks[0]

    # print(f"{player_one.joystick!r}, {player_two.joystick!r}")
    def new_ball():
        return Ball(10, screen_width, screen_height, 300, OPTION["BALL_COLOR"])
    
    ball = new_ball()
    net_texture = create_net_texture(5, screen_height)

    player_joystick_list = [player_one, player_two]

    for _, p in enumerate((player_one, player_two)):
        p.movement_key_dict[p.valid_movement_inputs[0]] = -240
        p.movement_key_dict[p.valid_movement_inputs[1]] = 240

    def render_player_score(player: str, player_score: int) -> pygame.Surface:
        return GameFont.Default.render(f"{player}{player_score}", False, Color.Black)

    def render_player_got_point(player_number: str) -> pygame.Surface:
        return GameFont.Default.render(f"Player {player_number} got the point!", False, Color.Black)

    def render_player_won(player_number: str) -> pygame.Surface:
        return GameFont.Default.render(f"Player {player_number} won the game!", False, Color.Black)

    player_one_score_text = render_player_score("", player_one.score)
    player_two_score_text = render_player_score("", player_two.score)
    player_one_got_point_text = render_player_got_point("One")
    player_two_got_point_text = render_player_got_point("Two")

    # TODO: alternate the responsibility of resuming the game between the players.
    paused_text = GameFont.Default.render("Press the Spacebar or the A button to begin!", False, Color.Black)

    game_state = GameState.Paused

    running = True
    while running:
        dt = ms / 1000.0
        
        # Get user input.
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
                    ball = new_ball()
                    game_state = GameState.Paused

                # Quits back to the main menu
                if game_state == GameState.GameOver and event.key == K_SPACE:
                    running = False
                    break

                for player in player_joystick_list:
                    if event.key in player.valid_movement_inputs:
                        player.current_key = event.key

            if event.type == KEYUP:
                for player in player_joystick_list:
                    if event.key in player.valid_movement_inputs:
                        test = player.movement_key_dict.get(event.key, 0)
                        current = player.movement_key_dict.get(player.current_key, 0)
                        if -test - current != 0:
                            player.current_key = 0

            # Similar to key-down events. Only real difference is that I need to get the ID
            # of the joystick before doing something with the input.
            if event.type == JOYBUTTONDOWN:

                # Resumes the Game. This happens after the player gets a point.
                if game_state == GameState.Paused and \
                        event.button == XboxButton.A:
                    game_state = GameState.Start

                # Pauses the game when the player gets a point.
                if game_state == GameState.PlayerGotPoint and \
                        event.button == XboxButton.A:
                    ball = new_ball()
                    game_state = GameState.Paused

                # Quits out of the game. This happens when the game is over.
                if game_state == GameState.GameOver and \
                        event.button == XboxButton.A:
                    running = False
                    break
            
            if event.type == JOYHATMOTION:
                for p in player_joystick_list:
                    p_id = p.joystick.get_instance_id()
                    if p.joystick is not None and \
                            event.instance_id == p_id:
                        if event.value == (0, 1):
                            p.current_key = K_w if p_id == 0 else K_UP
                        elif event.value == (0, -1):
                            p.current_key = K_s if p_id == 0 else K_DOWN
                        else:
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
        screen.blit(player_two_score_text, [screen_width // 2 + 20, 20])

        # Draw the players to the screen.
        player_one.draw_to(screen)
        player_two.draw_to(screen)

        # Draw the ball to the screen.
        ball.draw_to(screen)

        # Display the "player got point" or winning text for each player.
        if ball.exited_right_border:
            screen.blit(player_one_got_point_text, [(screen_width / 2) - (player_one_got_point_text.get_width() // 2),
                                                    screen_height / 2])
        elif ball.exited_left_border:
            screen.blit(player_two_got_point_text, [(screen_width / 2) - (player_two_got_point_text.get_width() // 2),
                                                    screen_height / 2])

        # Tick the clock at the set frame rate.
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
