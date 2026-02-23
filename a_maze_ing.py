"""Main entry point for the A-Maze-Ing application.

This script acts as the coordinator for the entire pipeline:
1. Loads and validates the configuration file.
2. Generates a maze (perfect or imperfect).
3. Solves the maze.
4. Saves the results to an output file.
5. Visualizes the maze using MiniLibX.
"""

from mazegen import load_config
from mazegen import MazeGenerator
from mazegen import MazeSolver
from mazegen import save_maze
from mazegen.interface import MazeDraw


def main() -> None:
    """Orchestrates the maze generation, solving, and visualization process.

    Reads configuration from the command line, executes the generation
    and solving algorithms, writes the output to a file, and launches
    the graphical interface. Handles configuration errors gracefully.
    """
    try:
        config = load_config()

        generator = MazeGenerator(
            config["HEIGHT"], config["WIDTH"], config.get("SEED")
        )
        generator.generate_maze(
            config["PERFECT"], config["ENTRY"], config["EXIT"]
        )

        solver = MazeSolver(generator.grid)
        path = solver.solve_maze(config["ENTRY"], config["EXIT"])
        save_maze(solver.grid, path, config)

        screen = MazeDraw(
            "A-Maze-Ing", generator.grid, config["ENTRY"], config["EXIT"], path
        )
        screen.draw()
    except ValueError as e:
        print(e)
    except OSError as e:
        print(f"ERROR: Could not write to file: {e}")


if __name__ == "__main__":
    main()
