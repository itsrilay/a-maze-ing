from unittest.mock import patch, mock_open
from mazegen.load_config import load_config
import sys
import pytest


def test_load_config_valid() -> None:
    """Tests loading a valid configuration file.

    Verifies that the configuration dictionary is correctly populated
    when the file contains all mandatory keys and valid values.
    """
    test_args = ["prog_name", "fake_config.txt"]

    mock_data = (
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True"
    )
    with patch.object(sys, 'argv', test_args):
        with patch("builtins.open", new=mock_open(read_data=mock_data)):
            assert load_config() == {
                "WIDTH": 20,
                "HEIGHT": 15,
                "ENTRY": (0, 0),
                "EXIT": (19, 14),
                "OUTPUT_FILE": "maze.txt",
                "PERFECT": True
            }


def test_load_config_missing_key() -> None:
    """Tests loading a configuration with a missing mandatory key.

    Verifies that the program exits gracefully (SystemExit) when
    a required key (e.g., EXIT) is absent.
    """
    test_args = ["prog_name", "fake_config.txt"]

    # Missing EXIT
    mock_data = (
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True"
    )
    with patch.object(sys, 'argv', test_args):
        with patch("builtins.open", new=mock_open(read_data=mock_data)):
            with pytest.raises(SystemExit):
                load_config()


def test_load_config_negative_height() -> None:
    """Tests loading a configuration with an invalid negative dimension.

    Verifies that the program exits gracefully when a dimension like
    HEIGHT is a negative integer.
    """
    test_args = ["prog_name", "fake_config.txt"]

    mock_data = (
        "WIDTH=20\n"
        "HEIGHT=-15\n"
        "ENTRY=0,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True"
    )
    with patch.object(sys, 'argv', test_args):
        with patch("builtins.open", new=mock_open(read_data=mock_data)):
            with pytest.raises(SystemExit):
                load_config()


def test_load_config_invalid_coordinate_format() -> None:
    """Tests loading a configuration with malformed coordinates.

    Verifies that the program exits gracefully when a coordinate pair
    contains non-numeric strings (e.g., 'nice,hello').
    """
    test_args = ["prog_name", "fake_config.txt"]

    mock_data = (
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=nice,hello\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True"
    )
    with patch.object(sys, 'argv', test_args):
        with patch("builtins.open", new=mock_open(read_data=mock_data)):
            with pytest.raises(SystemExit):
                load_config()


def test_load_config_negative_coordinate() -> None:
    """Tests loading a configuration with negative coordinates.

    Verifies that the program exits gracefully when a coordinate pair
    contains negative integers, which are invalid for array indexing.
    """
    test_args = ["prog_name", "fake_config.txt"]

    mock_data = (
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=-1,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True"
    )
    with patch.object(sys, 'argv', test_args):
        with patch("builtins.open", new=mock_open(read_data=mock_data)):
            with pytest.raises(SystemExit):
                load_config()


def test_load_config_file_not_found() -> None:
    """Tests loading a non-existent configuration file.

    Verifies that the program exits gracefully when the specified
    configuration file cannot be opened.
    """
    test_args = ["prog_name", "missing_config.txt"]

    with patch.object(sys, 'argv', test_args):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(SystemExit):
                load_config()


def test_load_config_bad_syntax() -> None:
    """Tests loading a configuration file with invalid syntax.

    Verifies that the program exits gracefully when a line does not
    follow the 'KEY=VALUE' format (e.g., using a colon).
    """
    test_args = ["prog_name", "missing_config.txt"]

    mock_data = "WIDTH:20\nHEIGHT=15"
    with patch.object(sys, 'argv', test_args):
        with patch("builtins.open", new=mock_open(read_data=mock_data)):
            with pytest.raises(SystemExit):
                load_config()
