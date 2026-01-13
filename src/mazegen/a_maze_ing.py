import sys
from typing import Any


def parse_value(value: str) -> Any:
    """Parses a string value into a specific type (int, bool, or tuple).

    Args:
        value (str): The string value to be parsed.

    Returns:
        Any: The parsed value. It returns an int if the string is numeric,
        a bool if it is 'True' or 'False', a tuple of ints if it is a
        coordinate pair (e.g., '1,2'), or the original string otherwise.
    """
    if value.isdigit():
        return int(value)
    elif value == "True":
        return True
    elif value == "False":
        return False
    try:
        x, y = value.split(",")
        if x.strip().isdigit() and y.strip().isdigit():
            return (int(x), int(y))
        else:
            sys.exit("ERROR: Invalid coordinate values.")
    except ValueError:
        return value


def load_config() -> dict[str, Any]:
    """Loads configuration from the file specified in command-line arguments.

    Reads the file line by line, skipping comments and empty lines. It parses
    key-value pairs and converts values to appropriate types.

    Returns:
        dict[str, Any]: A dictionary containing the configuration settings.

    Raises:
        SystemExit: If a line is not a valid key-value pair.
    """
    config: dict[str, Any] = {}

    try:
        filename = sys.argv[1]
    except IndexError:
        sys.exit(
            "ERROR: No configuration file provided. " +
            "\nUsage: python3 a_maze_ing.py <config_file>"
        )

    try:
        with open(filename) as file:
            for line in file:
                if line.strip().startswith("#") or line.strip() == "":
                    continue
                try:
                    key, value = line.strip().split("=", 1)
                    config[key.upper()] = parse_value(value)
                except ValueError:
                    sys.exit("ERROR: Expected 'KEY=VALUE' pair")
    except FileNotFoundError:
        sys.exit(f"ERROR: Configuration file '{filename}' not found.")

    return config


def main() -> None:
    """Entry point for the application script."""
    config = load_config()
    print(config)


if __name__ == "__main__":
    main()
