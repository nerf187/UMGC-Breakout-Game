import sys
import os
import types
import pytest

#
# Allow imports from project root
#
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core import config
from Managers.collisionManager import collisionManager
from Objects.ball import Ball
from Objects.paddle import Paddle
from Objects.block import Block


def test_check_ball_walls_left_right_top(monkeypatch):
    #
    # make screen small and test left/right/top collisions
    #
    monkeypatch.setattr(config, "SCREEN_WIDTH", 100)
    monkeypatch.setattr(config, "SCREEN_HEIGHT", 80)

    #
    # left wall
    #
    b = Ball(x=1, y=40, radius=5, vx=-1, vy=0)
    collisionManager.check_ball_walls(b)
    assert b.x == pytest.approx(b.radius)
    assert b.vx == pytest.approx(abs(-1.0))

    #
    # right wall
    #
    b = Ball(x=200, y=40, radius=5, vx=1, vy=0)
    collisionManager.check_ball_walls(b)
    assert b.x == pytest.approx(config.SCREEN_WIDTH - b.radius)
    assert b.vx == pytest.approx(-abs(1.0))

    #
    # top wall
    #
    b = Ball(x=50, y=1, radius=5, vx=0, vy=-1)
    collisionManager.check_ball_walls(b)
    assert b.y == pytest.approx(b.radius)
    assert b.vy == pytest.approx(abs(-1.0))


def test_check_ball_paddle_bounce_and_no_bounce():
    p = Paddle(x=50.0, y=100.0, width=20, height=10, speed=10)

    #
    # ball moving down should bounce
    #
    b = Ball(x=50.0, y=104.0, radius=5, vx=0, vy=1)
    bounced = collisionManager.check_ball_paddle(b, p)
    assert bounced is True
    assert b.vy < 0  # now moving up

    # 
    # positioned above paddle per implementation
    #
    px, py, pw, ph = p.rect()
    assert b.y == pytest.approx(py - b.radius - 1)

    # 
    # ball moving up should not trigger bounce
    #
    b2 = Ball(x=50.0, y=104.0, radius=5, vx=0, vy=-1)
    bounced2 = collisionManager.check_ball_paddle(b2, p)
    assert bounced2 is False


def test_check_ball_blocks_destroys_and_scores():
    # 
    # Block at (0,0) size 10x10; ball centered will collide and destroy it
    #
    block = Block(x=0, y=0, width=10, height=10, hp=1, score=123)
    b = Ball(x=5.0, y=5.0, radius=6, vx=0, vy=1)

    remaining, score_inc = collisionManager.check_ball_blocks(b, [block])
    assert score_inc == 123
    assert remaining == []


def test_check_ball_bottom(monkeypatch):
    #
    # Check ball voids at the bottom of the screen as expected
    #
    monkeypatch.setattr(config, "SCREEN_HEIGHT", 50)
    b = Ball(x=10, y=100, radius=5, vx=0, vy=1)
    assert collisionManager.check_ball_bottom(b) is True
