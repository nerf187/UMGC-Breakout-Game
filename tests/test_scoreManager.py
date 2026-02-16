import sys
import os
import pytest

# 
# Allow imports from project root
#
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Managers.scoreManager import scoreManager


def get_levels_dir():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(repo_root, 'Assets', 'levels')


def test_level_exists_and_load():
    levels_dir = get_levels_dir()
    sm = scoreManager(levels_dir=levels_dir)
    
    # 
    # Expect level1 to exist in the provided assets
    #
    assert sm.level_exists(1) is True

    loaded = sm.load_level(1)
    assert loaded is True
    assert sm.level is not None
    assert isinstance(sm.blocks, list)

    info = sm.get_level_info()
    assert info.get('number') == 1
    assert 'blocks_count' in info


def test_next_level_and_available_levels():
    levels_dir = get_levels_dir()
    sm = scoreManager(levels_dir=levels_dir)

    # 
    # load first level then go to next
    #
    assert sm.load_level(1) is True
    has_next, msg = sm.next_level()

    # 
    # Either loads next level or reports no more levels; ensure handled gracefully
    #
    assert isinstance(has_next, bool)
    assert isinstance(msg, str)

    avail = sm.get_available_levels()
    assert isinstance(avail, list)


def test_level_completion_percentage_changes_after_removing_blocks():
    levels_dir = get_levels_dir()
    sm = scoreManager(levels_dir=levels_dir)
    assert sm.load_level(1) is True

    pct_before = sm.get_level_completion_percentage()
    assert pct_before == pytest.approx(0.0)

    # 
    # simulate destroying one block
    #
    if sm.blocks:
        sm.blocks.pop()
    pct_after = sm.get_level_completion_percentage()
    assert pct_after >= 0.0
    assert pct_after != pct_before


def test_load_all_available_levels():
    """Attempt to load every level file found in the levels directory.

    This test will iterate the available level numbers discovered by
    `scoreManager.count_available_levels()` and call `load_level` for each.
    It asserts that every level that exists can be loaded successfully.
    """
    levels_dir = get_levels_dir()
    sm = scoreManager(levels_dir=levels_dir)

    total = sm.count_available_levels()

    # 
    # If there are no levels, skip the assertion but ensure function is callable
    #
    if total == 0:
        pytest.skip("No levels found in Assets/levels to test")

    failures = []
    for n in range(1, total + 1):
        if not sm.level_exists(n):
            failures.append((n, "missing"))
            continue

        ok = sm.load_level(n)
        if not ok:
            failures.append((n, "failed to load"))

    assert failures == [], f"Some levels failed to load: {failures}"
