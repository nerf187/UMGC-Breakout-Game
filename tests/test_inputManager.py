import sys
import os
from types import SimpleNamespace
import pytest

# 
# Allow imports from project root
#
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import importlib
im = importlib.import_module('Managers.inputManager')
from Managers.game_state import GameState
from Objects.paddle import Paddle


def setup_dummy_pygame(module):
    pg = SimpleNamespace()
    # 
    # basic keys
    #
    pg.K_SPACE = 32
    pg.K_LEFT = 0
    pg.K_a = 1
    pg.K_RIGHT = 2
    pg.K_d = 3
    pg.K_ESCAPE = 27
    pg.K_UP = 38
    pg.K_DOWN = 40
    pg.K_RETURN = 13
    pg.K_p = ord('p')
    pg.K_r = ord('r')

    # 
    # event type constants
    #
    pg.KEYDOWN = 1000
    pg.QUIT = 1001

    # default key getter (returns no keys pressed)
    class KeyMap(dict):
        def __getitem__(self, k):
            return dict.get(self, k, False)

    pg.key = SimpleNamespace()
    pg.key.get_pressed = lambda: KeyMap()

    module.pygame = pg
    return pg


def test_check_launch_ball_true_false():
    pg = setup_dummy_pygame(im)

    keys = {pg.K_SPACE: True}
    assert im.inputManager.check_launch_ball(keys, ball_launched=False) is True
    # 
    # if already launched, should remain False
    #
    assert im.inputManager.check_launch_ball(keys, ball_launched=True) is False


def test_handle_game_input_moves_when_playing(monkeypatch):
    pg = setup_dummy_pygame(im)

    # simulate left key pressed; use the default KeyMap so missing keys return False
    keys_map = im.pygame.key.get_pressed()
    keys_map[pg.K_LEFT] = True
    im.pygame.key.get_pressed = lambda: keys_map

    p = Paddle(x=50.0, y=10.0, width=20, height=6, speed=10)
    im.inputManager.handle_game_input([], GameState.PLAYING, p, dt=0.5)
    assert p.x < 50.0


def test_handle_state_transitions_menu_and_quit():
    pg = setup_dummy_pygame(im)

    # 
    # menu space -> open level select
    #
    ev = SimpleNamespace()
    ev.type = pg.KEYDOWN
    ev.key = pg.K_SPACE
    state, running, action = im.inputManager.handle_state_transitions([ev], GameState.MENU, True)
    assert state == GameState.LEVEL_SELECT
    assert running is True
    assert action == "open_level_select"

    # 
    # quit event
    #
    ev2 = SimpleNamespace()
    ev2.type = pg.QUIT
    state2, running2, action2 = im.inputManager.handle_state_transitions([ev2], GameState.PLAYING, True)
    assert running2 is False
    assert action2 == "quit"
