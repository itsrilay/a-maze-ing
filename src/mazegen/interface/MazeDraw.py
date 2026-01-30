from mazegen.interface.MazeInterface import MazeInterface
from mazegen.common import Direction


class MazeDraw:
    """
    Class for drawing the maze on the screen.
    """
    def __init__(self, title: str,
                 grid: list[list[int]],
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 solution: list[tuple[int, int]] | None = None,
                 screen_size: tuple[int, int] = (800, 800)) -> None:
        """
        Initialize MazeDraw with grid and configuration.

        :param title: Title of the window.
        :param grid: 2D list representing the maze.
        :param entry: Coordinates of the entry point.
        :param exit: Coordinates of the exit point.
        :param solution: List of coordinates representing the solution path.
        :param screen_size: Tuple (width, height) of the screen.
        """
        self._mlx: MazeInterface = MazeInterface()
        self._grid = grid
        self._entry = entry
        self._exit = exit
        self.solution = solution
        self.width: int = screen_size[0]
        self.height: int = screen_size[1]
        self.r_center: tuple[int, int] = (0, 0)
        self.r_w: int = 0
        self.r_h: int = 0
        self._mlx.init_screen(title, self.width, self.height)

    def draw_rect(self, coords: tuple[int, int],
                  width: int, height: int, color: int) -> None:
        """
        Draw a filled rectangle.

        :param coords: Top-left coordinates (x, y).
        :param width: Width of the rectangle.
        :param height: Height of the rectangle.
        :param color: Color of the rectangle.
        """
        for x in range(width):
            for y in range(height):
                self._mlx.my_mlx_put_pixel(
                    (coords[0] + x, coords[1] + y), color)

    def draw_cube(self, coords: tuple[int, int],
                  side_len: int, color: int) -> None:
        """
        Draw a square (cube).

        :param coords: Top-left coordinates (x, y).
        :param side_len: Length of the square side.
        :param color: Color of the square.
        """

        for x in range(side_len):
            for y in range(side_len):
                self._mlx.my_mlx_put_pixel(
                    (coords[0] + x, coords[1] + y), color)

    def draw_solution(self, side_len: int,
                      offset_x: int, offset_y: int) -> None:
        """
        Draw the solution path.

        :param side_len: Length of the square side.
        :param offset_x: X offset on screen.
        :param offset_y: Y offset on screen.
        """
        if not self.solution:
            return

        color_solution = 0xFF0000FF  # Blue
        solution_thick = max(1, side_len // 3)
        margin = (side_len - solution_thick) // 2

        for (c, r) in self.solution:
            x = offset_x + c * side_len + margin
            y = offset_y + r * side_len + margin

            self.draw_cube((x, y), solution_thick, color_solution)

    def draw_maze(self) -> None:
        """
        Draw the maze based on the grid and relative measures.
        """
        rows = len(self._grid)
        cols = len(self._grid[0])

        cell_w = self.r_w // cols
        cell_h = self.r_h // rows
        side_len = min(cell_w, cell_h)

        offset_x = self.r_center[0] + (self.r_w - side_len * cols) // 2
        offset_y = self.r_center[1] + (self.r_h - side_len * rows) // 2

        color_entry = 0xFF00FF00
        color_exit = 0xFFFF0000
        color_path = 0xFFFFFFFF
        color_wall = 0xFF000000

        wall_thick = max(1, side_len // 8)

        for r in range(rows):
            for c in range(cols):
                x = offset_x + c * side_len
                y = offset_y + r * side_len

                if (c, r) == self._entry:
                    color = color_entry
                elif (c, r) == self._exit:
                    color = color_exit
                else:
                    color = color_path

                self.draw_cube((x, y), side_len, color)

                cell_mask = self._grid[r][c]

                if cell_mask & Direction.NORTH:
                    self.draw_rect((x, y), side_len, wall_thick, color_wall)
                if cell_mask & Direction.SOUTH:
                    self.draw_rect(
                        (x, y + side_len - wall_thick),
                        side_len, wall_thick, color_wall
                    )
                if cell_mask & Direction.WEST:
                    self.draw_rect((x, y), wall_thick, side_len, color_wall)
                if cell_mask & Direction.EAST:
                    self.draw_rect(
                        (x + side_len - wall_thick, y),
                        wall_thick, side_len, color_wall
                    )

        if self.solution:
            self.draw_solution(side_len, offset_x, offset_y)

        self._mlx.mlx_put_image_to_window(
            self._mlx.mlx_ptr,
            self._mlx.win_ptr,
            self._mlx.img_ptr,
            0,
            0
        )

    def get_relative_measures(self) -> None:
        """
        Calculate relative screen measures for the maze area.
        """
        self.r_w = (self.width * 90) // 100
        self.r_h = (self.height * 85) // 100
        self.r_center = ((self.width * 5) // 100,
                         (self.height * 5) // 100)

    def draw(self) -> None:
        """
        Main draw loop: setup measures, draw maze, and start loop.
        """
        try:
            self.get_relative_measures()
            self.draw_maze()
            self._mlx.mlx_loop(self._mlx.mlx_ptr)
        except Exception as erro:
            print(f"Error {erro}\nFunction draw MazeDraw.py")
