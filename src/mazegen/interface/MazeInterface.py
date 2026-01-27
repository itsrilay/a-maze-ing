from mlx import Mlx
from typing import Any, Optional
import sys


class MazeInterface(Mlx):
    """
    Class for Drawing and Handling interface
    """

    def __init__(self) -> None:
        super().__init__()
        self.img_data: Optional[memoryview] = None
        self.bpp: int = 0
        self.size_line: int = 0

    def init_screen(self,
                    title: str,
                    grid: list[list[int]],
                    rows: int,
                    cols: int,
                    width: int = 800,
                    height: int = 800) -> None:
        """
        Initialize the MLX window and start the loop.
        """
        try:
            # Init unit measures
            self.width: int = width
            self.height: int = height
            self.grid_data = grid
            self.rows_data = rows
            self.cols_data = cols

            # Init Maze vars
            self.mlx_ptr: Any = self.mlx_init()
            self.win_ptr: Any = self.mlx_new_window(self.mlx_ptr,
                                                    self.width,
                                                    self.height,
                                                    title)
            self.mlx_clear_window(self.mlx_ptr, self.win_ptr)

            # Setup image for efficient drawing
            self.img_ptr = self.mlx_new_image(self.mlx_ptr,
                                              self.width,
                                              self.height)

            # Get image data address
            data = self.mlx_get_data_addr(self.img_ptr)
            self.img_data = data[0]
            self.bits_per_pixel = data[1]
            self.line_lenght = data[2]
            self.endian = data[3]

            self.handle_hook()

        except Exception as error:
            print(f"Error initializing screen: {error}")
            sys.exit(1)

    def exit_window(self) -> None:
        """
        Clean up and destroy the window.
        """
        try:
            if hasattr(self, 'img_ptr'):
                self.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
            if hasattr(self, 'win_ptr'):
                self.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            if hasattr(self, 'mlx_ptr'):
                self.mlx_loop_exit(self.mlx_ptr)

            print("Closing window...")

        except Exception as error:
            print(f"Error exiting window: {error}")
            sys.exit(1)

    def handle_hook(self) -> None:
        """
        Setup input hooks.
        """
        def mymouse(button: int, x: int, y: int, param: Optional[Any]) -> None:
            print(f"Got mouse event! button {button} at {x},{y}.")

        def mykey(keynum: int, param: Optional[Any]) -> None:
            print(f"Got key {keynum}")
            if keynum == 113 or keynum == 65307 or keynum == 53:
                self.exit_window()

        self.mlx_mouse_hook(self.win_ptr, mymouse, None)
        self.mlx_key_hook(self.win_ptr, mykey, None)

        self.mlx_hook(self.win_ptr, 17, 0, self.exit_window, None)
