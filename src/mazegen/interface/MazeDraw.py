from src.mazegen.interface.MazeInterface import MazeInterface


class MazeDraw(MazeInterface):
    """
    """
    def my_mlx_put_pixel(self, coords: tuple[int, int], color: int) -> None:
        """
        Docstring for my_mlx_put_pixel
        coords is the coordinates to print the value
        """
        x, y = coords
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.line_lenght) + (x * 4)
            self.img_data[offset:offset+4] = color.to_bytes(4, 'little')

    def draw_cube(self, coords: tuple[int, int],
                  side_len: int, color: int):
        """
        Docstring for draw_cube
        """
        for x in range(side_len):
            for y in range(side_len):
                self.my_mlx_put_pixel((x, y), color)

        self.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr,
                                     self.img_ptr, coords[0],
                                     coords[1])

    def draw_maze(self, rows: int, cols: int) -> None:
        """
        Lógica simplificada: Desenha uma linha horizontal para debug.
        """
        color = 0xFFFF00FF  # Opaque White
        self.draw_cube((self.width // 2, self.height // 2),
                       40,
                       color)

    def draw(self,
             title: str,
             grid: list[list[int]],
             rows: int,
             cols: int,
             width: int = 800,
             height: int = 800):
        """
        Docstring for draw

        :param self: Description
        """
        self.init_screen(title,
                         grid,
                         rows,
                         cols,
                         width,
                         height)
        self.draw_maze(rows, cols)

        self.mlx_loop(self.mlx_ptr)
