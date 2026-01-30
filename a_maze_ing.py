from mazegen.load_config import load_config
from mazegen.MazeGenerator import MazeGenerator
from mazegen.MazeSolver import MazeSolver
from mazegen.writer import save_maze
from mazegen.interface.MazeDraw import MazeDraw


def main() -> None:
    """Entry point for the application script."""
    try:
        config = load_config()
        print(config)

        generator = MazeGenerator(config["HEIGHT"], config["WIDTH"])
        generator.generate_maze(
            config["PERFECT"], config["ENTRY"], config["EXIT"]
        )

        solver = MazeSolver(generator.grid)
        path = solver.solve_maze(config["ENTRY"], config["EXIT"])
        save_maze(solver.grid, path, config)
        print(solver.grid)

        screen = MazeDraw(
            "A-Maze-Ing", generator.grid, config["ENTRY"], config["EXIT"], path
        )
        screen.draw()
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
