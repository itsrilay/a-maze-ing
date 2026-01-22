from mazegen.common import DIRECTION_OFFSETS
from mazegen.common import MazeConfig


def save_maze(
    grid: list[list[int]],
    path: list[tuple[int, int]],
    config: MazeConfig
) -> None:
    """Writes the maze grid, entry/exit, and solution path to a file.

    The output format consists of:
    1. The grid walls in hexadecimal (one digit per cell).
    2. An empty line.
    3. The Entry coordinates (x,y).
    4. The Exit coordinates (x,y).
    5. The solution path as a sequence of directional letters (N, E, S, W).

    Args:
        grid (list[list[int]]): The maze grid bitmasks.
        path (list[tuple[int, int]]): The solution path coordinates.
        config (MazeConfig): The configuration containing output filename
                                and entry/exit points.
    """
    # Reverse lookup to find the Direction Enum from a coordinate tuple
    reversed_offsets = {v: k for k, v in DIRECTION_OFFSETS.items()}

    with open(config["OUTPUT_FILE"], "w") as file:
        # Write the Grid
        for row in grid:
            for col in row:
                # Use f-string with :X to format integer as uppercase Hex
                file.write(f"{col:X}")
            file.write("\n")
        file.write("\n")

        file.write(f"{config['ENTRY'][0]},{config['ENTRY'][1]}\n")
        file.write(f"{config['EXIT'][0]},{config['EXIT'][1]}\n")

        for i in range(len(path) - 1):
            curr = path[i]
            next_cell = path[i + 1]

            # Calculate the direction vector (dx, dy)
            dx = next_cell[0] - curr[0]
            dy = next_cell[1] - curr[1]

            # Look up the Direction enum and get its name (e.g., "NORTH")
            direction_enum = reversed_offsets[(dx, dy)]

            # Write the first letter of the name (e.g., "N")
            file.write(direction_enum.name[0])
