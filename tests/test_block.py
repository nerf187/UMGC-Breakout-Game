import sys
import os

# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Objects.block import Block


def test_block_initialization():
    block = Block(10, 20, 40, 15, type="normal", hp=2, score=150, color="#FFFFFF")

    assert block.x == 10
    assert block.y == 20
    assert block.width == 40
    assert block.height == 15
    assert block.type == "normal"
    assert block.hp == 2
    assert block.score == 150
    assert block.color == "#FFFFFF"


def test_block_rect():
    block = Block(5, 6, 30, 12)

    rect = block.rect()

    assert rect == (5, 6, 30, 12)


def test_block_hit_reduces_hp():
    block = Block(0, 0, 20, 10, hp=2)

    destroyed = block.hit()

    assert block.hp == 1
    assert destroyed is False


def test_block_destroyed_when_hp_zero():
    block = Block(0, 0, 20, 10, hp=1)

    destroyed = block.hit()

    assert block.hp == 0
    assert destroyed is True


def test_block_multiple_hits():
    block = Block(0, 0, 20, 10, hp=2)

    block.hit()
    destroyed = block.hit()

    assert block.hp == 0
    assert destroyed is True
