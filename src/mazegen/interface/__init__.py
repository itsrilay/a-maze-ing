"""The interface sub-package for maze visualization.

This package handles the graphical display of the maze using the MiniLibX
library. It provides classes for window management, user input handling,
and drawing the maze structure and solution path.
"""

from mazegen.interface.MazeDraw import MazeDraw
from mazegen.interface.MazeInterface import MazeInterface

__all__ = ["MazeDraw", "MazeInterface"]
