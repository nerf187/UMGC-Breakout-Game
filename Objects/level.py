#
# Level loader that parses JSON level files and constructs Block objects.
#
import json
from typing import List
from Core import config
from Objects.block import Block


class Level:
    def __init__(self, width: int, height: int, tile_size: int, blocks: List[Block]):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.blocks = blocks

    #
    # Load a level from a JSON file.
    # Expected JSON structure:
    # {
    #   "width": 800,
    #   "height": 600,
    #   "tile_size": 40,
    #   "blocks": [ {"x":0,"y":0,"type":"normal","hp":1,...}, ... ]
    # }
    #
    @staticmethod
    def from_file(path: str) -> "Level":
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        width = int(data.get("width", config.SCREEN_WIDTH))
        height = int(data.get("height", config.SCREEN_HEIGHT))
        tile_size = int(data.get("tile_size", config.TILE_SIZE))

        raw_blocks = data.get("blocks", [])
        blocks: List[Block] = []

        for idx, entry in enumerate(raw_blocks):
            try:
                gx = int(entry["x"])  # grid x
                gy = int(entry["y"])  # grid y
            except Exception as e:
                raise ValueError(f"Invalid block entry at index {idx} in {path}: {e}")

            px = gx * tile_size
            py = gy * tile_size
            w = int(entry.get("width", tile_size))
            h = int(entry.get("height", tile_size))
            btype = entry.get("type", "normal")
            hp = int(entry.get("hp", 1))
            score = int(entry.get("score", 100))
            color = entry.get("color", "#FFFFFF")

            #
            # Basic bounds check (grid-based)
            #
            if gx < 0 or gy < 0:
                raise ValueError(f"Block at index {idx} has negative grid coordinates: {gx},{gy}")
            # if gx < 0 or gy < 0:

            blocks.append(Block(px, py, w, h, btype, hp, score, color))
        # for idx, entry in enumerate(raw_blocks):

        return Level(width, height, tile_size, blocks)
