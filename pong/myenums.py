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
