"""Shared constants and type definitions for the maze generation system.

This module defines the configuration schema, direction enumerations,
and movement offsets used throughout the package.
"""

from enum import IntEnum
from typing import TypedDict
from typing_extensions import NotRequired


class MazeConfig(TypedDict):
    """Configuration dictionary for maze generation settings.

    Attributes:
        WIDTH (int): The width of the maze in number of cells.
        HEIGHT (int): The height of the maze in number of cells.
        ENTRY (tuple[int, int]): The starting coordinates (x, y).
        EXIT (tuple[int, int]): The ending coordinates (x, y).
        OUTPUT_FILE (str): The path where the output maze will be saved.
        PERFECT (bool): True for a perfect maze (one path), False for loops.
        SEED (int | str | None): Optional seed for the random number generator
            to ensure reproducibility.
    """

    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: NotRequired[int | str | None]


class Direction(IntEnum):
    """Bitmask constants representing the four cardinal directions.

    Attributes:
        NORTH (int): Bitmask for North (1).
        EAST (int): Bitmask for East (2).
        SOUTH (int): Bitmask for South (4).
        WEST (int): Bitmask for West (8).
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


DIRECTION_OFFSETS = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0)
}
