"""The mazegen package.

This package provides a complete system for generating perfect and imperfect
mazes, solving them, and saving the results to files.
"""

from .MazeGenerator import MazeGenerator
from .MazeSolver import MazeSolver
from .load_config import load_config
from .writer import save_maze
from .common import MazeConfig

__all__ = [
    "MazeGenerator",
    "MazeSolver",
    "load_config",
    "save_maze",
    "MazeConfig"
]
