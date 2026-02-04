import os
import json
from typing import List, Optional, Tuple
from Core import config
from Objects.level import Level
from Objects.block import Block

class scoreManager:
    def __init__(self, levels_dir: str = None):
        self.levels_dir = levels_dir or self.get_default_levels_dir()
        self.current_level = 1
        self.total_levels = self.count_available_levels()
        self.level = None
        self.blocks = []
        
    def get_default_levels_dir(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "..", config.LEVELS_DIR)
    
    def count_available_levels(self) -> int:
        count = 0
        level_num = 1
        
        while True:
            level_path = self.get_level_path(level_num)
            if os.path.exists(level_path):
                count += 1
                level_num += 1
            else:
                break
        
        return count
    
    def get_level_path(self, level_num: int) -> str:
        return os.path.join(self.levels_dir, f"level{level_num}.json")
    
    def level_exists(self, level_num: int) -> bool:
        return os.path.exists(self.get_level_path(level_num))
    
    def load_level(self, level_num: int) -> bool:
        if not self.level_exists(level_num):
            return False
            
        try:
            level_path = self.get_level_path(level_num)
            self.level = Level.from_file(level_path)
            self.blocks = list(self.level.blocks)
            self.current_level = level_num
            return True
        except Exception as e:
            print(f"Error loading level {level_num}: {e}")
            return False
    
    def next_level(self) -> Tuple[bool, Optional[str]]:
        next_level_num = self.current_level + 1
        
        if self.level_exists(next_level_num):
            success = self.load_level(next_level_num)
            if success:
                return True, f"Level {next_level_num} loaded"
            else:
                return False, f"Failed to load level {next_level_num}"
        else:
            return False, "No more levels available"
    
    def reload_current_level(self) -> bool:
        return self.load_level(self.current_level)
    
    def reset_level_blocks(self) -> None:
        if self.level:
            self.blocks = list(self.level.blocks)
    
    def get_level_info(self) -> dict:
        if not self.level:
            return {}
            
        return {
            "number": self.current_level,
            "blocks_count": len(self.blocks),
            "total_blocks": len(self.level.blocks) if self.level else 0,
            "width": self.level.width if self.level else 0,
            "height": self.level.height if self.level else 0,
            "tile_size": self.level.tile_size if self.level else 0
        }
    
    def get_block_types_summary(self) -> dict:
        summary = {}
        if not self.level:
            return summary
            
        for block in self.level.blocks:
            block_type = block.type
            summary[block_type] = summary.get(block_type, 0) + 1
        
        return summary
    
    def has_levels(self) -> bool:
        return self.total_levels > 0
    
    def is_last_level(self) -> bool:
        return self.current_level >= self.total_levels
    
    def get_level_completion_percentage(self) -> float:
        if not self.level or len(self.level.blocks) == 0:
            return 0.0
        
        remaining = len(self.blocks)
        total = len(self.level.blocks)
        destroyed = total - remaining
        
        return (destroyed / total) * 100.0 if total > 0 else 0.0
