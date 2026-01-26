from mazegen.MazeGenerator import MazeGenerator


def test_maze_dimensions() -> None:
    """Tests that the generated maze has the correct dimensions."""
    width = 20
    height = 15
    generator = MazeGenerator(height=height, width=width)

    # Generate the maze (we need to run this to populate the grid fully,
    # though __init__ creates the empty grid)
    generator.generate_maze(is_perfect=True, entry=(0, 0), exit=(1, 1))

    assert len(generator.grid) == height
    assert all(len(row) == width for row in generator.grid)


def test_maze_reproducibility() -> None:
    """Tests that providing a seed produces identical mazes."""
    seed = "42"
    width = 10
    height = 10

    gen1 = MazeGenerator(height=height, width=width, seed=seed)
    gen1.generate_maze(is_perfect=True, entry=(0, 0), exit=(1, 1))

    gen2 = MazeGenerator(height=height, width=width, seed=seed)
    gen2.generate_maze(is_perfect=True, entry=(0, 0), exit=(1, 1))

    assert gen1.grid == gen2.grid


def test_maze_randomness() -> None:
    """Tests that different seeds produce different mazes."""
    width = 10
    height = 10

    gen1 = MazeGenerator(height=height, width=width, seed="seed_A")
    gen1.generate_maze(is_perfect=True, entry=(0, 0), exit=(1, 1))

    gen2 = MazeGenerator(height=height, width=width, seed="seed_B")
    gen2.generate_maze(is_perfect=True, entry=(0, 0), exit=(1, 1))

    # There is a tiny statistical chance this fails, but it's vanishingly small
    assert gen1.grid != gen2.grid
