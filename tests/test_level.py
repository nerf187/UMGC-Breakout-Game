# Tests/test_level_simple.py
import json
import tempfile
import os
import sys

# Setup imports for your structure
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from Objects.level import Level
    print("Imports working")
except ImportError:
    print("Failed to import Level from Objects.level")
    sys.exit(1)

def run_test():    
    # 1. Create a test level file
    level_json = {
        "width": 400,
        "height": 300,
        "tile_size": 20,
        "blocks": [
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 2, "y": 0}
        ]
    }
    
    # Save it
    test_file = "test_level.json"
    with open(test_file, "w") as f:
        json.dump(level_json, f)
    
    print("\nCreated test file: test_level.json")
    
    try:
        # 2. Load it
        level = Level.from_file(test_file)
        
        # 3. Check results
        print(f"Level size: {level.width}x{level.height}")
        print(f"Tile size: {level.tile_size}")
        print(f"Blocks: {len(level.blocks)}")
        
        # Show block positions
        for i, block in enumerate(level.blocks[:3]):  # First 3 blocks
            print(f"Block {i}: grid({level_json['blocks'][i]['x']},{level_json['blocks'][i]['y']})")
            print(f"\t -> pixels({block.x},{block.y})")
        
        # Verify grid-to-pixel conversion
        success = True
        for i, block in enumerate(level.blocks):
            expected_x = level_json['blocks'][i]['x'] * level.tile_size
            expected_y = level_json['blocks'][i]['y'] * level.tile_size
            
            if block.x != expected_x or block.y != expected_y:
                print(f"   Block {i} position wrong!")
                print(f"   Expected: ({expected_x}, {expected_y})")
                print(f"   Got: ({block.x}, {block.y})")
                success = False
            else:
                print(f"Block {i} position correct")
        
        if success:
            print("\nSUCCESS! Level loading works correctly!")
        else:
            print("\nSome issues found in pixel conversion.")
        
        return success
        
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\nCleaned up {test_file}")

if __name__ == "__main__":
    print("=" * 50)
    print("Quick Level Test")
    print("=" * 50)
    
    if run_test():
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure