from unittest.mock import patch, mock_open
from mazegen.a_maze_ing import load_config
import sys


def test_load_config() -> None:
    """Tests the load_config function with mocked arguments.

    Verifies that the configuration dictionary is correctly populated from
    a simulated file containing valid key-value pairs.
    """
    test_args = ["prog_name", "fake_config.txt"]

    mock_data = "WIDTH=20\nHEIGHT=15"
    with patch.object(sys, 'argv', test_args):
        with patch("builtins.open", new=mock_open(read_data=mock_data)):
            assert load_config() == {"WIDTH": 20, "HEIGHT": 15}
