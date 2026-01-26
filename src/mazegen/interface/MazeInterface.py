from mlx import Mlx
from typing import Any, Optional
import sys


class MazeInterface(Mlx):
    """
    Class for Drawing and Handling interface
    """

    def __init__(self):
        super().__init__()

    def init_screen(self,
                    title: str,
                    width: int = 800,
                    height: int = 800) -> None:
        """
        Initialize the MLX window and start the loop.
        """
        try:
            # Init unit measures
            self.width: int = width
            self.height: int = height

            # Init Maze vars
            self.mlx_ptr: Any = self.mlx_init()
            self.win_ptr: Any = self.mlx_new_window(self.mlx_ptr,
                                                    self.width,
                                                    self.height,
                                                    title)

            # Setup image (if needed for drawing pixels directly later)
            self.img_ptr = self.mlx_new_image(self.mlx_ptr,
                                              self.width,
                                              self.height)

            # Clear window (black background usually)
            self.mlx_clear_window(self.mlx_ptr, self.win_ptr)

            # Setup hooks and initial drawing
            self.handle_hook()
            self.draw_sentence()

            # Start the main loop
            self.mlx_loop(self.mlx_ptr)
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

    def draw_sentence(self) -> None:
        """
        Draw a test sentence on the screen.
        """

        white_color = 0xFFFFFF
        self.mlx_string_put(self.mlx_ptr, self.win_ptr, 20, 20, white_color,
                            "Hello PyMlx!")

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