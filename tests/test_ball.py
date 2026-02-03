# tests/test_ball.py
import math
import pytest
import sys
import os

# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core import config
from Objects.ball import Ball

def test_initialization():
    # test ball initialization with explicit parameters
    ball = Ball(x=100.0, y=200.0, radius=config.BALL_RADIUS, speed=config.BALL_SPEED, vx=0.5, vy=0.5)
    assert ball.x == 100.0
    assert ball.y == 200.0
    assert ball.radius == config.BALL_RADIUS
    assert ball.speed == config.BALL_SPEED
    assert ball.vx == pytest.approx(0.5 / math.sqrt(0.5))
    assert ball.vy == pytest.approx(0.5 / math.sqrt(0.5))

def test_init_normalizes_velocity():
    # create a Ball with vx/vy values.
    b = Ball(x=0, y=0, vx=3, vy=4)

    assert b.vx == pytest.approx(0.6)
    assert b.vy == pytest.approx(0.8)
    assert math.hypot(b.vx, b.vy) == pytest.approx(1.0)


def test_init_zero_velocity_defaults_upwards():
    # If someone creates a ball with vx=0 and vy=0 (no direction),
    # the Ball class should force it to move upward so it doesn't get stuck.
    b = Ball(x=0, y=0, vx=0, vy=0)

    assert b.vx == pytest.approx(0.0)
    assert b.vy == pytest.approx(-1.0)
    assert math.hypot(b.vx, b.vy) == pytest.approx(1.0)


def test_update_moves_ball():
    # update(0.5) should move the ball right by 5 when speed=10 and vx=1
    b = Ball(x=0, y=0, speed=10.0, vx=1, vy=0)

    b.update(dt=0.5)

    assert b.x == pytest.approx(5.0)
    assert b.y == pytest.approx(0.0)


def test_rect_dimensions():
    # checks that the ball’s collision box is the right size and in the right position.
    b = Ball(x=10.9, y=20.1, radius=3, speed=1.0, vx=1, vy=0)

    left, top, w, h = b.rect()

    assert (w, h) == (6, 6)
    assert left == int(b.x - b.radius)
    assert top == int(b.y - b.radius)

def test_velocity_normalization():
    # test that velocity is always normalized
    ball = Ball(x=100, y=200, vx=3, vy=4, speed=100)
    magnitude = math.hypot(ball.vx, ball.vy)
    assert magnitude == pytest.approx(1.0)