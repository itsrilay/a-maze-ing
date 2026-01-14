from mazegen.load_config import load_config


def main() -> None:
    """Entry point for the application script."""
    config = load_config()
    print(config)


if __name__ == "__main__":
    main()
