from enum import Enum

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4
    LIFE_LOST = 5