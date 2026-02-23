"""MLX window management and event hook utilities.

This module provides the MazeInterface class, which wraps the MiniLibX
Mlx base class to manage window lifecycle, off-screen image rendering,
and keyboard event dispatch for the maze visualiser.
"""

from mlx import Mlx
from typing import Any, Optional
import sys


class MazeInterface(Mlx):
    """Manages the MLX window lifecycle and provides drawing utilities.

    Inherits from Mlx to expose MiniLibX functions directly. Extends the
    base class with window initialisation, off-screen image rendering,
    and a dispatching key-event registry.

    Attributes:
        key_callbacks: Mapping of X11 keysym codes to zero-argument
            callables. Populated externally before the event loop starts.
        bpp: Bits per pixel — kept for backwards compatibility.
        size_line: Image row size in bytes — kept for backwards compat.
    """

    def __init__(self) -> None:
        """Initialize MazeInterface with an empty key-callback registry."""
        super().__init__()
        self.bpp: int = 0
        self.size_line: int = 0
        self.key_callbacks: dict[int, Any] = {}

    def init_screen(
        self, title: str, width: int, height: int
    ) -> None:
        """Initialize the MLX window and off-screen image buffer.

        Creates the MLX context, a titled window, and an off-screen
        image for double-buffered rendering. Registers default event
        hooks for keyboard, mouse, and window-close events.

        Args:
            title: Text displayed in the window title bar.
            width: Window width in pixels.
            height: Window height in pixels.
        """
        try:
            self.width: int = width
            self.height: int = height
            self.mlx_ptr: Any = self.mlx_init()
            self.win_ptr: Any = self.mlx_new_window(
                self.mlx_ptr, self.width, self.height, title
            )
            self.mlx_clear_window(self.mlx_ptr, self.win_ptr)
            self.img_ptr: Any = self.mlx_new_image(
                self.mlx_ptr, self.width, self.height
            )
            data = self.mlx_get_data_addr(self.img_ptr)
            self.img_data: memoryview = data[0]
            self.bits_per_pixel: int = data[1]
            self.line_length: int = data[2]
            self.endian: int = data[3]
            self.handle_hook()
        except Exception as error:
            print(f"Error initializing screen: {error}")
            sys.exit(1)

    def exit_window(self) -> None:
        """Destroy all MLX resources and terminate the event loop."""
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
        """Register MLX hooks for keyboard, mouse, and window close.

        Keyboard events are first looked up in ``key_callbacks``; any
        key not found there triggers the built-in ESC/Q exit logic.
        """
        def mymouse(
            button: int, x: int, y: int, param: Optional[Any]
        ) -> None:
            """Handle mouse button events (currently a no-op).

            Args:
                button: Mouse button identifier.
                x: Cursor x-coordinate at the time of the event.
                y: Cursor y-coordinate at the time of the event.
                param: Optional user-data pointer passed by MLX (unused).
            """
            pass

        def mykey(keynum: int, param: Optional[Any]) -> None:
            """Dispatch a key event to a registered callback or exit.

            Args:
                keynum: X11 keysym code of the pressed key.
                param: Optional user-data pointer passed by MLX (unused).
            """
            if keynum in self.key_callbacks:
                self.key_callbacks[keynum]()
                return
            if keynum in (113, 81, 65307, 53):
                self.exit_window()

        self.mlx_mouse_hook(self.win_ptr, mymouse, None)
        self.mlx_key_hook(self.win_ptr, mykey, None)
        self.mlx_hook(self.win_ptr, 17, 0, self.exit_window, None)

    def my_mlx_put_pixel(
        self, coords: tuple[int, int], color: int
    ) -> None:
        """Write a single pixel to the off-screen image buffer.

        Args:
            coords: Pixel position as (x, y).
            color: 32-bit colour in 0xAARRGGBB format.
        """
        x, y = coords
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.line_length) + (x * 4)
            self.img_data[offset:offset + 4] = color.to_bytes(
                4, 'little'
            )
