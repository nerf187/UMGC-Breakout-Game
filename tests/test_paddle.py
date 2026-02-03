# paddle tests: check that Paddle moves correctly, stays on screen, and reports its hitbox.
# tests/test_paddle.py
import pytest
import sys
import os
# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core import config
from Objects.paddle import Paddle
import Objects.paddle as paddle_mod

def test_initialization():
    # Test that paddle initializes with correct values
    p = Paddle(x=50.0, y=100.0, width=config.PADDLE_WIDTH, height=config.PADDLE_HEIGHT, speed=config.PADDLE_SPEED)
    assert p.x == 50.0
    assert p.y == 100.0
    assert p.width == config.PADDLE_WIDTH
    assert p.height == config.PADDLE_HEIGHT
    assert p.speed == config.PADDLE_SPEED

def test_move_changes_x():
    # moving right should increase x based on speed and time.
    p = Paddle(x=50, y=10, width=20, height=5, speed=10)
    p.move(direction=1, dt=0.5)
    assert p.x == pytest.approx(55.0)

def test_move_negative_direction():
    # moving left should decrease X
    p = Paddle(x=50, y=10, width=20, height=5, speed=10)
    p.move(direction=-1, dt=0.5)
    assert p.x == pytest.approx(45.0)

def test_move_zero_direction():
    # test that zero direction doesn't move paddle"""
    p = Paddle(x=50, y=10, width=20, height=5, speed=10)
    p.move(direction=0, dt=1.0)
    assert p.x == pytest.approx(50.0)

def test_move_clamps_left_edge(monkeypatch):
    # moving left too far should stop at the left edge of the screen.
    monkeypatch.setattr(paddle_mod.config, "SCREEN_WIDTH", 100)
    p = Paddle(x=50, y=10, width=20, height=5, speed=1000)
    p.move(direction=-1, dt=1.0)
    assert p.x == pytest.approx(p.width / 2)

def test_move_clamps_right_edge(monkeypatch):
    # moving right too far should stop at the right edge of the screen.
    monkeypatch.setattr(paddle_mod.config, "SCREEN_WIDTH", 100)
    p = Paddle(x=50, y=10, width=20, height=5, speed=1000)
    p.move(direction=1, dt=1.0)
    assert p.x == pytest.approx(100 - (p.width / 2))


def test_rect_returns_expected_tuple():
    # rect() should return the paddle's collision box (left, top, width, height)
    p = Paddle(x=50, y=10, width=20, height=6, speed=10)
    assert p.rect() == (int(50 - 10), int(10 - 3), 20, 6)

