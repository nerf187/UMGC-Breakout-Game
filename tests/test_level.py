# tests/test_level.py
import pytest
import sys
import os
import json

# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core import config
from Objects.level import Level
from Objects.block import Block

def test_from_file_basic(tmp_path):
    """Test loading a basic level from JSON"""
    level_data = {
        "width": 800,
        "height": 600,
        "tile_size": 40,
        "blocks": [
            {"x": 0, "y": 0, "type": "normal", "hp": 1},
            {"x": 1, "y": 0, "type": "hard", "hp": 2, "score": 200, "color": "#FF0000"}
        ]
    }
        
    temp_file = tmp_path / "test_level.json"
    temp_file.write_text(json.dumps(level_data))

    level = Level.from_file(temp_file)

    assert level.width == 800
    assert level.height == 600
    assert level.tile_size == 40
    assert len(level.blocks) == 2


def test_from_file_invalid_coordinates(tmp_path):
        # Test loading level with invalid coordinates
    level_data = {
        "blocks": [
            {"x": -1, "y": 0}  # Negative x should raise error
        ]
    }
        
    temp_file = tmp_path / "test_level.json"
    temp_file.write_text(json.dumps(level_data))
    with pytest.raises(ValueError, match="negative grid coordinates"):
        Level.from_file(temp_file)
        
def test_all_levels_load():
    #
    # Test that every levelX.json file in assets/ can be loaded.
    # Assumes assets/ is at project root.
    #
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = config.LEVELS_DIR
    
    # find all level files
    level_files = []
    for fname in os.listdir(assets_dir):
        if fname.startswith("level") and fname.endswith(".json"):
            level_files.append(os.path.join(assets_dir, fname))
    
    # skip if no levels found
    # if not level_files:
        # pytest.skip("No level files found in assets/")
    
    # test each level
    for level_path in level_files:
        level_name = os.path.basename(level_path)
        
        assert os.path.exists(level_path), f"{level_name} does not exist"
        with open(level_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            assert isinstance(data, dict), f"{level_name}: not a JSON object"
        
        level = Level.from_file(level_path)
        
        # level has required attributes
        assert hasattr(level, "width"), f"{level_name}: missing width"
        assert hasattr(level, "height"), f"{level_name}: missing height"
        assert hasattr(level, "tile_size"), f"{level_name}: missing tile_size"
        assert hasattr(level, "blocks"), f"{level_name}: missing blocks"
        
        # attributes have valid values
        assert level.width > 0, f"{level_name}: width must be positive"
        assert level.height > 0, f"{level_name}: height must be positive"
        assert level.tile_size > 0, f"{level_name}: tile_size must be positive"
        assert isinstance(level.blocks, list), f"{level_name}: blocks must be a list"
        
        # check each block
        for i, block in enumerate(level.blocks):
            assert isinstance(block, Block), f"{level_name}: block {i} is not a Block"
            assert block.x >= 0, f"{level_name}: block {i} has negative x"
            assert block.y >= 0, f"{level_name}: block {i} has negative y"
            assert block.width > 0, f"{level_name}: block {i} has invalid width"
            assert block.height > 0, f"{level_name}: block {i} has invalid height"
            assert block.hp >= 1, f"{level_name}: block {i} has invalid hp"
            assert block.score >= 0, f"{level_name}: block {i} has negative score"
            
            # color is valid hex
            assert block.color.startswith("#"), f"{level_name}: block {i} color missing #"
            assert len(block.color) == 7, f"{level_name}: block {i} color should be #RRGGBB"
            try:
                int(block.color[1:], 16)  # parse hex
            except ValueError:
                pytest.fail(f"{level_name}: block {i} has invalid hex color: {block.color}")
        
        print(f"✓ {level_name}: loaded {len(level.blocks)} blocks")

def test_level_file_not_found():
    #
    # Level.from_file should raise an error or handle missing file.
    # Test with non-existent file
    with pytest.raises(Exception):
        Level.from_file("non_existent_level.json")

def test_level_invalid_json(tmp_path):
    #
    # Test that invalid JSON raises appropriate error.
    # Create a temp file with invalid JSON
    bad_file = tmp_path / "bad_level.json"
    bad_file.write_text("{ invalid json")
    
    with pytest.raises(json.JSONDecodeError):
        Level.from_file(str(bad_file))

