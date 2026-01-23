from collections import deque
from mazegen.common import DIRECTION_OFFSETS


class MazeSolver:
    """
    A class to solve mazes using the Breadth-First Search (BFS) algorithm.

    Attributes:
        grid (list[list[int]]): A 2D grid representing the maze, where each
                                cell value is a bitmask of closed walls.
        width (int): The width of the maze grid.
        height (int): The height of the maze grid.
    """

    def __init__(self, grid: list[list[int]]):
        """Initialize the MazeSolver with a maze grid.

        Args:
            grid (list[list[int]]): The maze grid to solve.
        """
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)

    def solve_maze(
        self,
        entry: tuple[int, int],
        exit: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Finds the shortest path from entry to exit using BFS.

        Explores the maze layer by layer to guarantee the shortest path.
        It respects walls defined in the grid and returns the path coordinates.

        Args:
            entry (tuple[int, int]): The starting coordinates (x, y).
            exit (tuple[int, int]): The target coordinates (x, y).

        Returns:
            list[tuple[int, int]]: A list of coordinates representing the
            path from entry to exit. Returns an empty list if no path is found.
        """
        queue: deque[tuple[int, int]] = deque([entry])
        predecessors: dict[tuple[int, int], tuple[int, int] | None] = {
            entry: None
        }

        while (len(queue)):
            curr_cell = queue.popleft()
            if curr_cell == exit:
                break
            for direction, offset in DIRECTION_OFFSETS.items():
                nx, ny = curr_cell[0] + offset[0], curr_cell[1] + offset[1]
                cx, cy = curr_cell
                if (0 <= nx < self.width and 0 <= ny < self.height and
                        (nx, ny) not in predecessors):
                    # Check if wall is OPEN (bitwise AND is 0)
                    if not self.grid[cy][cx] & direction:
                        predecessors[(nx, ny)] = (cx, cy)
                        queue.append((nx, ny))

        path: list[tuple[int, int]] = []
        if exit in predecessors:
            curr_node: tuple[int, int] | None = exit
            # Backtrack from the exit to the entry using the predecessors map
            while curr_node is not None:
                path.append(curr_node)
                curr_node = predecessors[curr_node]

        path = list(reversed(path))

        return path
