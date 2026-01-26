from mazegen.MazeSolver import MazeSolver


def test_solve_simple_path() -> None:
    """Tests finding a path in a simple 2x1 maze.

    Layout: [ (0,0) -> (1,0) ]
    (0,0): Open East. Walls: N, S, W. (1+4+8 = 13, Hex D)
    (1,0): Open West. Walls: N, E, S. (1+2+4 = 7,  Hex 7)
    """
    # 13 (1101) | 7 (0111)
    grid = [[13, 7]]

    solver = MazeSolver(grid)
    entry = (0, 0)
    exit = (1, 0)

    path = solver.solve_maze(entry, exit)

    assert path == [(0, 0), (1, 0)]


def test_solve_no_path() -> None:
    """Tests that the solver returns an empty list if no path exists.

    Layout: [ (0,0) | (1,0) ]
    Both cells have ALL walls closed (15).
    """
    grid = [[15, 15]]

    solver = MazeSolver(grid)
    entry = (0, 0)
    exit = (1, 0)

    path = solver.solve_maze(entry, exit)

    assert path == []
