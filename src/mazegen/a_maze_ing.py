from mazegen.load_config import load_config
from mazegen.generator import MazeGenerator


def main() -> None:
    """Entry point for the application script."""
    config = load_config()
    print(config)
    generator = MazeGenerator(config["HEIGHT"], config["WIDTH"])
    generator.generate_maze()


if __name__ == "__main__":
    main()
