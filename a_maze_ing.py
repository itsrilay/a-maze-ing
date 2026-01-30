from src.mazegen.load_config import load_config
from src.mazegen.MazeGenerator import MazeGenerator
from src.mazegen.MazeSolver import MazeSolver
from src.mazegen.writer import save_maze
from src.mazegen.interface.MazeDraw import MazeDraw
import sys


def main() -> None:
    """Entry point for the application script."""
    try:
        config = load_config()
        print(config)

        height = config["HEIGHT"]
        width = config["WIDTH"]
        entry_tup = config["ENTRY"]
        exit_tup = config["EXIT"]
        perfect = config["PERFECT"]

        generator = MazeGenerator(height, width)
        generator.generate_maze(perfect, entry_tup, exit_tup)

        solver = MazeSolver(generator.grid)
        path = solver.solve_maze(entry_tup, exit_tup)
        save_maze(solver.grid, path, config)
        print(solver.grid)
        screen = MazeDraw()
        screen.draw("Amazing", generator.grid, height, width)
    except ValueError as e:
        sys.exit(e)


if __name__ == "__main__":
    main()
