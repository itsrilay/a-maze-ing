from mazegen.load_config import load_config
from mazegen.MazeGenerator import MazeGenerator
from mazegen.MazeSolver import MazeSolver
from mazegen.writer import save_maze


def main() -> None:
    """Entry point for the application script."""
    config = load_config()
    print(config)
    generator = MazeGenerator(config["HEIGHT"], config["WIDTH"])
    generator.generate_maze(config["PERFECT"], config["ENTRY"], config["EXIT"])
    solver = MazeSolver(generator.grid)
    path = solver.solve_maze(config["ENTRY"], config["EXIT"])
    save_maze(solver.grid, path, config)


if __name__ == "__main__":
    main()
