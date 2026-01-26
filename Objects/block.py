#
# Block dataclass used by Level loader and game logic.
#
from dataclasses import dataclass
from typing import Tuple


#
# Block dataclass
#
@dataclass
class Block:
    x: int
    y: int
    width: int
    height: int
    type: str = "normal"
    hp: int = 1
    score: int = 100
    color: str = "#BE0A0A"

    #
    # Get the block's rectangle as (x, y, width, height)
    #
    def rect(self) -> Tuple[int, int, int, int]:
        return (int(self.x), int(self.y), int(self.width), int(self.height))  # return rect tuple

    def __init__(self, x: int, y: int, width: int, height: int, type: str = "normal", hp: int = 1, score: int = 100, color: str = "#BE0A0A"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.hp = hp
        self.score = score
        self.color = color

    #
    # Apply damage to the block. Returns True if block is destroyed.
    #
    def hit(self) -> bool:
        self.hp -= 1
        return self.hp <= 0  # return destroyed status

    #
    # Concise debug representation
    #
    def __repr__(self) -> str:
        return f"Block(type={self.type},hp={self.hp},score={self.score},pos=({self.x},{self.y}))"  # return string repr
