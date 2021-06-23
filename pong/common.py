import pygame
import pygame.font
import pygame.surface


class GameFont:
    Default = pygame.font.Font("resource/fonts/lunchds.ttf", 30)
    Title = pygame.font.Font("resource/fonts/lunchds.ttf", 50)
    Arrow = pygame.font.Font("resource/fonts/lunchds.ttf", 80)


# Color class. Has named attributes of various colors I use often.
class Color:
    Black = 0, 0, 0, 255
    White = 255, 255, 255, 255
    Gray = 124, 124, 124, 255
    Red = 200, 50, 0, 255
    Blue = 0, 100, 200, 255
    Green = 0, 255, 0, 255
    DarkGreen = 7, 75, 21, 255
    Silver = 192, 192, 192, 255


# "Enum" that keeps track of the state of the menu.
class MenuState:
    val_range = range(0, 4)
    (Menu,
     Options,
     Game,
     Quit) = val_range


# "Enum" that keeps track of the game's state.
class GameState:
    val_range = range(0, 5)
    (Start,
     PlayerGotPoint,
     GameOver,
     Paused,
     Menu,) = val_range


# "Enum" that has values for each of the buttons on an Xbox One controller.
class XboxButton:
    val_range = range(0, 6)
    (A,
     X,
     Y,
     B,
     RB,
     LB) = val_range


class TextBox(object):
    """
    TextBox class. This is my base class for GUI objects. When instantiated, it
    will draw a rectangle to the screen with some text on it. The text can be
    centered using its center_text function. A custom text position within the
    TextBox can also be set.
    """
    def __init__(self,
                 pos: list,
                 size: list,
                 background_color: list,
                 text: str = "",
                 text_pos: list = None,
                 text_size: int = 20,
                 text_color: tuple = Color.Black):
        from .options import OPTION
        
        self.pos = pos
        self.size = size
        self.background_color = background_color
        self.text = text
        self.text_pos = text_pos or [20, 20]
        self.text_size = text_size
        self.text_color = text_color

        self.font = pygame.font.Font(OPTION["FONT_PATH"], self.text_size)

        self.surf = pygame.Surface(self.size)
        self.rect = self.surf.get_rect(topleft=self.pos)

        
        self.__draw_to_self(self.font)
        self.__center_text()

    def draw_to(self, screen: pygame.surface.Surface):
        screen.blit(self.surf, self.rect)

    def update_text(self, new_pos: list = None):
        if new_pos is None:
            new_pos = self.text_pos
        self.surf.fill([0, 0, 0, 0])
        self.text_pos = new_pos
        self.surf.fill(self.background_color)
        self.surf.blit(self.text_render, self.text_pos)

    def __draw_to_self(self, font: pygame.font.Font):
        self.surf.fill(self.background_color)
        self.text_render = font.render(self.text, False, self.text_color)
        self.surf.blit(self.text_render, self.text_pos)

    def __center_text(self):
        self.surf.fill([0, 0, 0, 0])
        self.text_pos = [(self.size[0] // 2) - self.text_render.get_rect().centerx,
                         (self.size[1] // 2) - self.text_render.get_rect().centery]
        self.surf.fill(self.background_color)
        self.surf.blit(self.text_render, self.text_pos)
