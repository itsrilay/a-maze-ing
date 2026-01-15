from typing import Any, TypedDict, cast
import sys


class MazeConfig(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool


MANDATORY_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]


def contains_negative(value: int | tuple[int, int]) -> bool:
    """Checks if the configuration value contains invalid numeric data.

    Args:
        value (int | tuple[int, int]): The configuration value to check.
        Can be an int, or a tuple of ints.

    Returns:
        bool: True if a single integer is <= 0 (invalid for dimensions) or
        if any coordinate in a tuple is < 0 (invalid for positions).
    """
    if isinstance(value, int):
        # Dimensions (WIDTH/HEIGHT) must be strictly positive (> 0)
        if value <= 0:
            return True
    else:
        x, y = value
        # Coordinates (ENTRY/EXIT) can be 0 but cannot be negative
        if x < 0 or y < 0:
            return True
    return False


def validate_config(config: dict[str, Any]) -> None:
    """Validates the configuration dictionary for missing keys and errors.

    Ensures all mandatory keys are present and that numeric values
    (integers or tuples) do not contain invalid negative numbers or
    zeros where prohibited. Terminate program if validation fails.

    Args:
        config (dict[str, Any]): A dictionary containing the config settings.
    """

    # Types for a valid config
    schema = MazeConfig.__annotations__

    # Check for missing keys
    missing_keys = [k for k in MANDATORY_KEYS if k not in config.keys()]
    if missing_keys:
        keys = "\n".join(missing_keys)
        sys.exit(f"ERROR: Missing mandatory keys in config:\n{keys}")

    # Check for invalid values
    for key, value in config.items():
        # Validate type
        if key in schema:
            expected_type = schema[key]
            # isinstance() doesn't support generics like tuple[int, int]
            if expected_type == tuple[int, int]:
                expected_type = tuple
            if not isinstance(value, expected_type):
                sys.exit(
                    f"ERROR: Invalid value for {key} in config: " +
                    f"Expected: {expected_type}   Got: {type(value)}"
                )

        # Validate numeric value
        if isinstance(value, (int, tuple)):
            if contains_negative(value):
                sys.exit(f"ERROR: Negative integer for {key} in config")


def parse_value(value: str) -> Any:
    """Parses a string value into a specific type (int, bool, or tuple).

    Args:
        value (str): The string value to be parsed.

    Returns:
        Any: The parsed value. It returns an int if the string is numeric,
        a bool if it is 'True' or 'False', a tuple of ints if it is a
        coordinate pair (e.g., '1,2'), or the original string otherwise.
    """
    # Try to convert to int first.
    # This will convert "-5" to -5 successfully. We allow this here
    # and catch the logical error in validate_config later.
    try:
        return int(value)
    except ValueError:
        pass

    if value == "True":
        return True
    elif value == "False":
        return False

    # Attempt to parse coordinates "x,y"
    try:
        x, y = value.split(",")
        if x.strip().isdigit() and y.strip().isdigit():
            return (int(x), int(y))
        else:
            # Comma implies a coordinate, failure to parse means syntax error.
            sys.exit("ERROR: Invalid coordinate values in config.")
    except ValueError:
        # No comma found, return the raw string (e.g. filename)
        return value


def load_config() -> MazeConfig:
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
                # Skip comments (#) and empty lines
                if line.strip().startswith("#") or line.strip() == "":
                    continue
                try:
                    key, value = line.strip().split("=", 1)
                    config[key.upper()] = parse_value(value)
                except ValueError:
                    sys.exit("ERROR: Expected 'KEY=VALUE' pair in config")
    except FileNotFoundError:
        sys.exit(f"ERROR: Configuration file '{filename}' not found.")

    validate_config(config)

    return cast(MazeConfig, config)
