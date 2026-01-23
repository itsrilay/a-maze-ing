from typing import Any
from math import ceil
from mazegen.common import Direction, DIRECTION_OFFSETS
import random


OPPOSITE_DIR = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST
}


class MazeGenerator:
    """
    A class to generate mazes using the Recursive Backtracker algorithm.

    Attributes:
        width (int): The width of the maze grid.
        height (int): The height of the maze grid.
        grid (list[list[int]]): A 2D grid representing the maze, where each
                                cell value is a bitmask of closed walls.
    """

    def __init__(self, height: int, width: int, seed: Any = None) -> None:
        """Initialize the MazeGenerator with dimensions and an optional seed.

        Args:
            height (int): The height of the maze (number of rows).
            width (int): The width of the maze (number of columns).
            seed (Any, optional): A seed for the random number generator
                                  to ensure reproducibility. Defaults to None.
        """
        self.width = width
        self.height = height
        # Initialize grid with all walls closed (15 = 1111 in binary)
        self.grid = [
            [15 for _ in range(width)]
            for _ in range(height)
        ]
        random.seed(seed)

    def _make_imperfect(self) -> None:
        """Removes random internal walls to create loops in the maze.

        This method calculates a target number of walls to remove (5% of total
        cells) and iteratively removes walls between valid neighbors, ensuring
        connectivity is updated on both sides of the wall.
        """
        walls_to_remove = ceil((self.width * self.height) * 0.05)
        walls_removed = 0

        while walls_removed < walls_to_remove:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            direction = random.choice([Direction.EAST, Direction.SOUTH])
            nx = x + DIRECTION_OFFSETS[direction][0]
            ny = y + DIRECTION_OFFSETS[direction][1]

            # Check if the wall exists before trying to break it
            if self.grid[y][x] & direction:
                # Prevent breaking the outer boundary walls
                if nx == self.width or ny == self.height:
                    continue

                # Remove the wall from the current cell
                self.grid[y][x] -= direction

                # Remove the corresponding wall from the neighbor
                self.grid[ny][nx] -= OPPOSITE_DIR[direction]

                walls_removed += 1
            else:
                continue

    def get_unvisited_neighbors(
        self, x: int, y: int
    ) -> list[tuple[int, int, Direction]]:
        """Finds all unvisited neighbors for a given cell.

        Args:
            x (int): The x-coordinate of the current cell.
            y (int): The y-coordinate of the current cell.

        Returns:
            list[tuple[int, int, Direction]]: A list of tuples containing
            the coordinates (nx, ny) of unvisited neighbors and the
            direction to reach them.
        """
        neighbors: list[tuple[int, int, Direction]] = []
        for direction, offset in DIRECTION_OFFSETS.items():
            nx, ny = x + offset[0], y + offset[1]
            # Check bounds
            if 0 <= nx < self.width and 0 <= ny < self.height:
                # Check if the neighbor is unvisited (value is still 15)
                if self.grid[ny][nx] == 15:
                    neighbors.append((nx, ny, direction))
        return neighbors

    def generate_maze(
        self,
        is_perfect: bool,
        entry: tuple[int, int],
        exit: tuple[int, int]
    ) -> None:
        """Generates the maze structure and displays the result.

        Uses the Recursive Backtracker algorithm to create a perfect maze.
        If is_perfect is False, it subsequently removes random walls to
        create loops. Finally, it delegates visualization to display_maze.

        Args:
            is_perfect (bool): If True, generates a perfect maze (one path).
                               If False, generates an imperfect maze (loops).
            entry (tuple[int, int]): Coordinates (x, y) of the entrance.
            exit (tuple[int, int]): Coordinates (x, y) of the exit.
        """
        stack = [(0, 0)]

        while len(stack):
            cell = stack[-1]
            neighbors = self.get_unvisited_neighbors(cell[0], cell[1])
            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                # Break walls between current cell and chosen neighbor
                self.grid[cell[1]][cell[0]] -= direction
                self.grid[ny][nx] -= OPPOSITE_DIR[direction]
                stack.append((nx, ny))  # Move to neighbor
            else:  # Dead end
                stack.pop(-1)  # Backtrack

        if not is_perfect:
            self._make_imperfect()

        self.display_maze(entry, exit)

    def display_maze(
        self,
        entry: tuple[int, int],
        exit: tuple[int, int]
    ) -> None:
        """Prints a visual ASCII representation of the maze to the terminal.

        Iterates through the grid to render walls, corridors, and specific
        markers for the entrance and exit.

        Args:
            entry (tuple[int, int]): Coordinates (x, y) of the entrance.
            exit (tuple[int, int]): Coordinates (x, y) of the exit.
        """
        print(("+---" * self.width) + "+")

        for y in range(self.height):
            top_str = "|"
            for x in range(self.width):
                if (x, y) == entry:
                    top_str += " E "
                elif (x, y) == exit:
                    top_str += " X "
                else:
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
