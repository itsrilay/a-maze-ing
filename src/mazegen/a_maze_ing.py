import sys
from typing import Any


def parse_value(value: str) -> Any:
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
            sys.exit("CONFIG ERROR: Invalid coordinate values.")
    except ValueError:
        return value


def load_config() -> dict[str, Any]:
    config: dict[str, Any] = {}

    with open(sys.argv[1]) as file:
        for line in file:
            if line.strip().startswith("#") or line.strip() == "":
                continue
            try:
                key, value = line.strip().split("=", 1)
                config[key.upper()] = parse_value(value)
            except ValueError:
                sys.exit("CONFIG ERROR: Expected 'KEY=VALUE' pair")
    return config


def main() -> None:
    """
    Entry point for the application script.
    """
    config = load_config()
    print(config)


if __name__ == "__main__":
    main()
