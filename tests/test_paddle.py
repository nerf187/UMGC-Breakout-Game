# paddle tests: check that Paddle moves correctly, stays on screen, and reports its hitbox

import pytest
from Objects.paddle import Paddle
import Objects.paddle as paddle_mod


def test_move_changes_x():
    # moving right should increase x based on speed and time
    p = Paddle(x=50, y=10, width=20, height=5, speed=10)
    p.move(direction=1, dt=0.5)
    assert p.x == pytest.approx(55.0)


def test_move_clamps_left_edge(monkeypatch):
    # moving left too far should stop at the left edge of the screen
    monkeypatch.setattr(paddle_mod.config, "SCREEN_WIDTH", 100)

    p = Paddle(x=50, y=10, width=20, height=5, speed=1000)
    p.move(direction=-1, dt=1.0)

    assert p.x == pytest.approx(p.width / 2)


def test_move_clamps_right_edge(monkeypatch):
    # moving right too far should stop at the right edge of the screen
    monkeypatch.setattr(paddle_mod.config, "SCREEN_WIDTH", 100)

    p = Paddle(x=50, y=10, width=20, height=5, speed=1000)
    p.move(direction=1, dt=1.0)

    assert p.x == pytest.approx(100 - (p.width / 2))


def test_rect_returns_expected_tuple():
    # rect() should return the paddle's collision box (left, top, width, height)
    p = Paddle(x=50, y=10, width=20, height=6, speed=10)
    assert p.rect() == (int(50 - 10), int(10 - 3), 20, 6)


def test_repr_contains_basic_info():
    # makes sure repr() prints something useful (includes Paddle and the width)(extra test)
    p = Paddle(x=50, y=10, width=20, height=6, speed=10)
    s = repr(p)
    assert "Paddle(" in s
    assert "w=20" in s
