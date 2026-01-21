from typing import Any
from enum import IntEnum
import random


class Direction(IntEnum):
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


class MazeGenerator:
    def __init__(self, height: int, width: int, seed: Any = None) -> None:
        self.width = width
        self.height = height
        self.grid = [
            [15 for _ in range(width)]
            for _ in range(height)
        ]
        random.seed(seed)

    def get_unvisited_neighbors(
            self, x: int, y: int
    ) -> list[tuple[int, int, Direction]]:
        neighbors: list[tuple[int, int, Direction]] = []
        for direction, offset in DIRECTION_OFFSETS.items():
            nx, ny = x + offset[0], y + offset[1]
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx] == 15:
                    neighbors.append((nx, ny, direction))
        return neighbors

    def generate_maze(self):
        stack = [(0, 0)]
        opposite_dir = {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST
        }

        while (len(stack)):
            cell = stack[-1]
            neighbors = self.get_unvisited_neighbors(cell[0], cell[1])
            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                self.grid[cell[1]][cell[0]] -= direction
                self.grid[ny][nx] -= opposite_dir[direction]
                stack.append((nx, ny))
            else:
                stack.pop(-1)

        print(("+---" * self.width) + "+")

        for y in range(self.height):
            top_str = "|"
            for x in range(self.width):
                top_str += "   "
                if self.grid[y][x] & Direction.EAST:
                    top_str += "|"
                else:
                    top_str += " "
            print(top_str)
            bot_str = "+"
            for x in range(self.width):
                if self.grid[y][x] & Direction.SOUTH:
                    bot_str += "---"
                else:
                    bot_str += "   "
                bot_str += "+"
            print(bot_str)
