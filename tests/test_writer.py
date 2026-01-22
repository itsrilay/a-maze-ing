from unittest.mock import patch, mock_open
from mazegen.writer import save_maze
from mazegen.common import MazeConfig


def test_save_maze_content() -> None:
    """Tests that save_maze writes the correct format to the file."""

    # A simple 2x1 grid: [15, 0] (F, 0)
    grid = [[15, 0]]
    path = [(0, 0), (1, 0)]  # Moving East
    config: MazeConfig = {
        "WIDTH": 2,
        "HEIGHT": 1,
        "OUTPUT_FILE": "test_maze.txt",
        "ENTRY": (0, 0),
        "EXIT": (1, 0),
        "PERFECT": True,
    }

    # We expect:
    # F0\n      (The grid row)
    # \n        (Empty line)
    # 0,0\n     (Entry)
    # 1,0\n     (Exit)
    # E         (Path direction: (1,0)-(0,0) = (1,0) -> East)

    m = mock_open()
    with patch("builtins.open", m):
        save_maze(grid, path, config)

    handle = m()

    # Check all write calls
    # 1. Grid
    handle.write.assert_any_call("F")
    handle.write.assert_any_call("0")
    handle.write.assert_any_call("\n")

    # 2. Config
    handle.write.assert_any_call("0,0\n")
    handle.write.assert_any_call("1,0\n")

    # 3. Path
    # The direction from (0,0) to (1,0) is East
    handle.write.assert_any_call("E")
