from enum import Enum

class GameState(Enum):
    MENU = 0
    LEVEL_SELECT = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETE = 4
    GAME_OVER = 5
    LIFE_LOST = 6