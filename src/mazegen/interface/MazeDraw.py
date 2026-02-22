"""Maze drawing primitives and interactive rendering for MiniLibX.

This module provides the MazeDraw class, which handles all visual
rendering of the maze: cells, walls, solution-path overlay, the "42"
pattern, and an interactive key-binding legend.  Three colour themes
are available and can be cycled at runtime.
"""

from mazegen.interface.MazeInterface import MazeInterface
from mazegen.MazeGenerator import MazeGenerator
from mazegen.MazeSolver import MazeSolver
from mazegen.common import Direction

THEMES: list[dict[str, int]] = [
    {   # default: dark navy background, white walls
        "wall":       0xFFFFFFFF,
        "path":       0xFF00BFFF,
        "entry":      0xFF00FF00,
        "exit_":      0xFFFF0000,
        "pattern_42": 0xFF8A2BE2,
        "floor":      0xFF1A1A2E,
        "text":       0x00FFFFFF,
    },
    {   # golden: gold walls on dark amber
        "wall":       0xFFFFD700,
        "path":       0xFF00BFFF,
        "entry":      0xFF00FF00,
        "exit_":      0xFFFF4500,
        "pattern_42": 0xFF8A2BE2,
        "floor":      0xFF1A1500,
        "text":       0x00FFD700,
    },
    {   # neon: neon-green walls on near-black
        "wall":       0xFF39FF14,
        "path":       0xFFFF00FF,
        "entry":      0xFF00FFFF,
        "exit_":      0xFFFF073A,
        "pattern_42": 0xFFFFFF00,
        "floor":      0xFF080010,
        "text":       0x0039FF14,
    },
]

THEME_NAMES: list[str] = ["Default", "Golden", "Neon"]

_KEY_R_LOWER: int = 114
_KEY_R_UPPER: int = 82
_KEY_P_LOWER: int = 112
_KEY_P_UPPER: int = 80
_KEY_C_LOWER: int = 99
_KEY_C_UPPER: int = 67


class MazeDraw:
    """Renders the maze in an MLX window with interactive controls.

    Handles cell and wall drawing, solution-path overlay, "42"-pattern
    highlighting, and keyboard-driven interactions: regenerate (R),
    toggle path (P), cycle colour theme (C), and quit (Q / ESC).

    Args:
        title: Window title bar text.
        grid: 2-D list of cell bitmask values (0–15, or 31 for "42").
        entry: Entry cell coordinates (x, y).
        exit: Exit cell coordinates (x, y).
        solution: Optional list of (x, y) cells on the solution path.
        screen_size: Window dimensions as (width, height) in pixels.
    """

    def __init__(
        self,
        title: str,
        grid: list[list[int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        solution: list[tuple[int, int]] | None = None,
        screen_size: tuple[int, int] = (800, 800),
    ) -> None:
        """Initialize MazeDraw and open the MLX window.

        Args:
            title: Title displayed in the window title bar.
            grid: 2-D bitmask grid produced by MazeGenerator.
            entry: Entry cell (x, y).
            exit: Exit cell (x, y).
            solution: Optional path cells returned by MazeSolver.
            screen_size: (width, height) of the window in pixels.
        """
        self._mlx: MazeInterface = MazeInterface()
        self._grid: list[list[int]] = grid
        self._entry: tuple[int, int] = entry
        self._exit: tuple[int, int] = exit
        self.solution: list[tuple[int, int]] | None = solution
        self.width: int = screen_size[0]
        self.height: int = screen_size[1]
        self.r_center: tuple[int, int] = (0, 0)
        self.r_w: int = 0
        self.r_h: int = 0
        self.theme_index: int = 0
        self.show_path: bool = False
        self._mlx.init_screen(title, self.width, self.height)

    def draw_rect(
        self,
        coords: tuple[int, int],
        width: int,
        height: int,
        color: int,
    ) -> None:
        """Draw a filled rectangle into the image buffer.

        Args:
            coords: Top-left corner as (x, y).
            width: Rectangle width in pixels.
            height: Rectangle height in pixels.
            color: Fill colour in 0xAARRGGBB format.
        """
        for x in range(width):
            for y in range(height):
                self._mlx.my_mlx_put_pixel(
                    (coords[0] + x, coords[1] + y), color
                )

    def draw_cube(
        self,
        coords: tuple[int, int],
        side_len: int,
        color: int,
    ) -> None:
        """Draw a filled square into the image buffer.

        Args:
            coords: Top-left corner as (x, y).
            side_len: Side length of the square in pixels.
            color: Fill colour in 0xAARRGGBB format.
        """
        for x in range(side_len):
            for y in range(side_len):
                self._mlx.my_mlx_put_pixel(
                    (coords[0] + x, coords[1] + y), color
                )

    def _clear_image(self) -> None:
        """Fill the entire image buffer with the theme's floor colour."""
        theme = THEMES[self.theme_index]
        bg = theme["floor"].to_bytes(4, 'little')
        total = len(self._mlx.img_data)
        self._mlx.img_data[0:total] = bytearray(bg * (total // 4))

    def draw_solution(
        self,
        side_len: int,
        offset_x: int,
        offset_y: int,
        color: int,
    ) -> None:
        """Overlay the solution path onto the image buffer.

        Args:
            side_len: Cell size in pixels.
            offset_x: Horizontal pixel offset of the maze area.
            offset_y: Vertical pixel offset of the maze area.
            color: Path colour in 0xAARRGGBB format.
        """
        if not self.solution:
            return

        solution_thick = max(1, side_len // 3)
        margin = (side_len - solution_thick) // 2

        for (c, r) in self.solution:
            x = offset_x + c * side_len + margin
            y = offset_y + r * side_len + margin
            self.draw_cube((x, y), solution_thick, color)

    def draw_maze(self) -> None:
        """Render the full maze grid to the image buffer and window.

        Fills each cell with its theme colour (42-pattern, entry, exit,
        or floor), draws closed walls from the cell bitmask, overlays
        the solution path when ``show_path`` is True, then flushes the
        image to the MLX window.
        """
        rows = len(self._grid)
        cols = len(self._grid[0])
        theme = THEMES[self.theme_index]

        cell_w = self.r_w // cols
        cell_h = self.r_h // rows
        side_len = min(cell_w, cell_h)

        offset_x = self.r_center[0] + (self.r_w - side_len * cols) // 2
        offset_y = self.r_center[1] + (self.r_h - side_len * rows) // 2

        wall_thick = max(1, side_len // 8)

        for r in range(rows):
            for c in range(cols):
                x = offset_x + c * side_len
                y = offset_y + r * side_len
                cell_mask = self._grid[r][c]

                # 42-pattern cells have bit 4 set (value == 31 = 0x1F)
                if cell_mask & 0x10:
                    cell_color = theme["pattern_42"]
                elif (c, r) == self._entry:
                    cell_color = theme["entry"]
                elif (c, r) == self._exit:
                    cell_color = theme["exit_"]
                else:
                    cell_color = theme["floor"]

                self.draw_cube((x, y), side_len, cell_color)

                # Only use the lower 4 bits for wall presence
                wall_bits = cell_mask & 0x0F
                if wall_bits & Direction.NORTH:
                    self.draw_rect(
                        (x, y), side_len, wall_thick, theme["wall"]
                    )
                if wall_bits & Direction.SOUTH:
                    self.draw_rect(
                        (x, y + side_len - wall_thick),
                        side_len, wall_thick, theme["wall"],
                    )
                if wall_bits & Direction.WEST:
                    self.draw_rect(
                        (x, y), wall_thick, side_len, theme["wall"]
                    )
                if wall_bits & Direction.EAST:
                    self.draw_rect(
                        (x + side_len - wall_thick, y),
                        wall_thick, side_len, theme["wall"],
                    )

        if self.show_path and self.solution:
            self.draw_solution(
                side_len, offset_x, offset_y, theme["path"]
            )

        self._mlx.mlx_put_image_to_window(
            self._mlx.mlx_ptr,
            self._mlx.win_ptr,
            self._mlx.img_ptr,
            0,
            0,
        )

    def _draw_legend(self) -> None:
        """Draw the key-binding legend at the bottom of the window.

        Uses mlx_string_put to render text directly onto the window
        surface (on top of the maze image), showing available controls
        and current state.
        """
        theme = THEMES[self.theme_index]
        text_color = theme["text"]
        legend_y = self.height - 40
        path_status = "ON" if self.show_path else "OFF"
        theme_name = THEME_NAMES[self.theme_index]

        lines = [
            "R: New Maze  P: Toggle Path  C: Colour  Q/ESC: Quit",
            f"Theme: {theme_name}   Path: {path_status}",
        ]
        for i, line in enumerate(lines):
            self._mlx.mlx_string_put(
                self._mlx.mlx_ptr,
                self._mlx.win_ptr,
                10,
                legend_y + i * 15,
                text_color,
                line,
            )

    def _regenerate(self) -> None:
        """Generate a new random maze with the same dimensions and redraw."""
        try:
            rows = len(self._grid)
            cols = len(self._grid[0])
            gen = MazeGenerator(rows, cols)
            gen.generate_maze(True, self._entry, self._exit)
            self._grid = gen.grid
            solver = MazeSolver(self._grid)
            self.solution = solver.solve_maze(self._entry, self._exit)
            self._redraw()
        except Exception as error:
            print(f"Error regenerating maze: {error}")

    def _toggle_path(self) -> None:
        """Toggle the solution-path overlay on or off."""
        self.show_path = not self.show_path
        self._redraw()

    def _next_colour(self) -> None:
        """Cycle to the next colour theme and redraw."""
        self.theme_index = (self.theme_index + 1) % len(THEMES)
        self._redraw()

    def _redraw(self) -> None:
        """Clear the image buffer and re-render the current maze state."""
        try:
            self._clear_image()
            self.draw_maze()
            self._draw_legend()
        except Exception as error:
            print(f"Error during redraw: {error}")

    def get_relative_measures(self) -> None:
        """Compute pixel dimensions for the maze display area.

        Allocates 90 % of window width and 80 % of window height to
        the maze grid, reserving a 5 % margin on all sides and ~15 % at
        the bottom for the key-binding legend.
        """
        self.r_w = (self.width * 90) // 100
        self.r_h = (self.height * 80) // 100
        self.r_center = (
            (self.width * 5) // 100,
            (self.height * 5) // 100,
        )

    def draw(self) -> None:
        """Set up key callbacks, render the maze, and start the loop.

        Registers R/P/C keyboard handlers, performs the initial render,
        then enters the blocking MLX event loop. All exceptions are
        caught and printed without crashing the process.
        """
        try:
            self.get_relative_measures()

            # Register interactive key callbacks (lower and upper case)
            self._mlx.key_callbacks[_KEY_R_LOWER] = self._regenerate
            self._mlx.key_callbacks[_KEY_R_UPPER] = self._regenerate
            self._mlx.key_callbacks[_KEY_P_LOWER] = self._toggle_path
            self._mlx.key_callbacks[_KEY_P_UPPER] = self._toggle_path
            self._mlx.key_callbacks[_KEY_C_LOWER] = self._next_colour
            self._mlx.key_callbacks[_KEY_C_UPPER] = self._next_colour

            self._redraw()
            self._mlx.mlx_loop(self._mlx.mlx_ptr)
        except Exception as erro:
            print(f"Error {erro}\nFunction draw MazeDraw.py")
