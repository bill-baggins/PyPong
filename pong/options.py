import json
import os.path
from .common import Color

from json import JSONDecodeError


__DEFAULT_OPTION = {
    "WINNING_SCORE": 5,
    "NET_COLOR": Color.White,
    "BACKGROUND_COLOR": Color.DarkGreen,
    "PLAYER1_COLOR": Color.Red,
    "PLAYER2_COLOR": Color.Blue,
    "BALL_COLOR": Color.Black,
    "NUM_OF_PLAYERS": 2
}

def fill() -> dict:
    d = None
    try:
        file = open("options.json")
        d = json.load(file)
        file.close()
    except JSONDecodeError or FileNotFoundError:
        print("Failed to read options.json...using default settings.")
        d = __DEFAULT_OPTION
    
    return d or {}

OPTION = fill()

if OPTION == {}:
    OPTION = __DEFAULT_OPTION
