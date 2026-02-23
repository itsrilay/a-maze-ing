*This project has been created as part of the 42 curriculum by ruisilva, hroxo*

# A-Maze-ing

## Description
The goal of this project is to build a robust maze generator in Python. It takes a configuration file as input to create both perfect and imperfect mazes, solves them, and exports the data in a specific hexadecimal format.

Beyond the CLI tool, this project features a visualizer with user interactions and is structured as a reusable Python package for future integration.

## Instructions

This project includes a `Makefile` to automate common tasks.

### Installation
To install the project dependencies (using `uv`), run:

```bash
make install
```

### Usage
To generate and solve a maze using the default `config.txt`:

```bash
make run
```

### Development

* **Debug**: Run the program with the Python debugger (`pdb`).

```bash
make debug
```

* **Lint**: Check code quality with `flake8` and `mypy`.

```bash
make lint
```

* **Clean**: Remove temporary files and caches.

```bash
make clean
```

## Configuration
The program takes a configuration file with one `KEY=VALUE` pair per line.

| Key | Description | Example |
| :--- | :--- | :--- |
| `WIDTH` | Width of the maze (number of cells) | `WIDTH=20` |
| `HEIGHT` | Height of the maze | `HEIGHT=15` |
| `ENTRY` | Entrance coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Filename for the output | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` for a single path, `False` for loops | `PERFECT=True` |
| `SEED` | Optional seed for reproducible generation | `SEED=123` |

## Algorithms

### Generation: Recursive Backtracker
This project utilizes the **Recursive Backtracker** algorithm, a randomized implementation of Depth-First Search (DFS).

* **Mechanism**: The algorithm acts as a "miner" that carves passages by moving to random unvisited neighbors. It utilizes a stack to track the current path; when the miner reaches a dead end, it backtracks (pops from the stack) until a new unvisited neighbor is found.

* **Properties**: This approach generates "perfect" mazes, which are mathematically equivalent to spanning trees (graphs with no loops and a unique path between any two nodes).

* **Aesthetic**: The Recursive Backtracker is known for creating mazes with long, winding corridors and high complexity, making them challenging to solve manually.

### Solving: Breadth-First Search
To solve the maze, the program implements the **Breadth-First Search (BFS)** algorithm.

* **Mechanism**: BFS explores the maze layer by layer, expanding equally in all directions from the starting point. It uses a queue to manage the frontier of visited cells.

* **Optimality**: Because the maze is an unweighted grid (every step costs the same), BFS is mathematically guaranteed to find the shortest possible path from the entrance to the exit.

## Implementation Details

### 1. Maze Generation (`src/mazegen/generator.py`)

The generation process is handled by the `MazeGenerator` class. It follows a linear pipeline to ensure the maze is valid and structurally sound.

#### A. Grid Initialization (`__init__`)
We start by creating a "solid" block of walls.

```python
# Initialize grid with all walls closed (15 = 1111 in binary)
self.grid = [
    [15 for _ in range(width)]
    for _ in range(height)
]
```

* **The Logic**: Every cell starts as `15` (binary `1111`).

* **Bitmasks**: We use bits to represent walls: North (`1`), East (`2`), South (`4`), West (`8`). A value of `15` means all directions are blocked. We will "carve" the maze by subtracting these values.

#### B. The Recursive Backtracker (`generate_maze`)
This is the core engine. We use an explicit **stack** to track our path, which avoids Python's recursion limit.

```python
stack = [entry]

while len(stack):
    cell = stack[-1]
    neighbors = self.get_unvisited_neighbors(cell[0], cell[1])
    if neighbors:
        nx, ny, direction = random.choice(neighbors)
        # Break walls between current cell and chosen neighbor
        self.grid[cell[1]][cell[0]] -= direction
        self.grid[ny][nx] -= OPPOSITE_DIR[direction]
        stack.append((nx, ny))  # Move to neighbor
    else:  # Dead end
        stack.pop(-1)  # Backtrack
```

* **Carving**: When we find a valid neighbor, we knock down the wall between them. For example, if we move **North**, we subtract `1` from the current cell and `4` (South) from the neighbor.

* **Backtracking**: When `neighbors` is empty (a dead end), we `pop` from the stack to return to the previous cell and try a different path.

#### C. Creating Loops (`_make_imperfect`)
If the user requests an imperfect maze, we randomly remove extra walls to create cycles.

```python
# Check if the wall exists before trying to break it
if self.grid[y][x] & direction:
    # Prevent breaking the outer boundary walls
    if nx == self.width or ny == self.height:
        continue

    # Remove the wall from the current cell
        self.grid[y][x] -= direction

    # Remove the corresponding wall from the neighbor
        self.grid[ny][nx] -= OPPOSITE_DIR[direction]
```

* **Validation**: We verify a wall actually exists (`& direction`) and that we aren't breaking the outer boundary before removing it.

### 2. Solving (`src/mazegen/solver.py`)
To find the shortest path, we use Breadth-First Search (BFS).

#### A. The BFS Loop (`solve_maze`)
We use a `deque` (double-ended queue) for efficient popping from the front.

```python
queue: deque[tuple[int, int]] = deque([entry])
predecessors: dict[tuple[int, int], tuple[int, int] | None] = {
    entry: None
}

while (len(queue)):
    curr_cell = queue.popleft()
    if curr_cell == exit:
        break
    for direction, offset in DIRECTION_OFFSETS.items():
        # ... calculate neighbor coordinates (nx, ny) ...

        # Check if wall is OPEN (bitwise AND is 0)
        if not self.grid[cy][cx] & direction:
            predecessors[(nx, ny)] = (cx, cy)
            queue.append((nx, ny))
```

* **Wall Check**: Unlike generation, here we check if walls are **open**. If `self.grid[cy][cx] & direction` is `0`, the path is clear.

* **Predecessors**: We store where we came from (`predecessors[(nx, ny)] = current`). This allows us to backtrack from the exit to the start to reconstruct the path.


## Code Reusability

This project is structured as a reusable Python package named `mazegen`. You can integrate the maze generation and solving logic into your own projects. A wheel file (`mazegen-1.0.0-py3-none-any.whl`) is provided in the root directory for installation via `pip`.

### Usage Example

Here is a basic example of how to use the package:

```python
from mazegen import MazeGenerator, MazeSolver

# 1. Instantiate the generator with desired dimensions and settings
config = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (19, 14),
    "PERFECT": True,
    "SEED": 42
}
generator = MazeGenerator(config["HEIGHT"], config["WIDTH"], config["SEED"])

# 2. Generate the maze structure
generator.generate_maze(config["PERFECT"], config["ENTRY"], config["EXIT"])

# The generated grid is accessible via the 'grid' attribute
# This grid can be used for custom processing or visualization
maze_grid = generator.grid

# 3. Instantiate the solver with the generated grid
solver = MazeSolver(maze_grid)

# 4. Solve the maze to find the shortest path
# The entry and exit points are taken from the generator's config
solution_path = solver.solve_maze(config["ENTRY"], config["EXIT"])

if solution_path:
    print(f"Shortest path found: {solution_path}")
else:
    print("No path found.")

```

This example demonstrates how to:
*   Instantiate and use the `MazeGenerator`.
*   Pass custom parameters like size and seed.
*   Access the generated maze structure (`generator.grid`).
*   Find a solution using the `MazeSolver`.

## Team and Project Management

This project was developed by **ruisilva** and **hroxo** as part of the 42 curriculum.

### Roles and Collaboration
This project was a collaborative effort where each team member took the lead on distinct components:

*   **ruisilva**: Architected the core backend and project structure. This included implementing the maze generation algorithm (`MazeGenerator`), developing the pathfinding logic (`MazeSolver`), and establishing the foundational layout of the package.

*   **hroxo**: Led the development of the user-facing components. This involved building the graphical interface for maze visualization (`MazeDraw`) and integrating all the backend modules into the final, interactive application.

While each member had primary ownership of these areas, all code was peer-reviewed to ensure quality and a shared understanding of the entire codebase.

### Planning and Evolution
The project followed an agile approach. We started with a basic plan to implement the core maze generation and solving algorithms. The plan evolved to incorporate a graphical interface and package the logic as a reusable module, based on the project requirements. The initial focus on a robust algorithmic core allowed for a smooth transition to building the user-facing features.

### Retrospective
*   **What Worked Well**: The modular design, separating the generator, solver, and interface, proved to be highly effective. It allowed for parallel development and easier debugging. Using `uv` for dependency management also streamlined the development setup.
*   **What Could Be Improved**: In the future, we could expand the project to include more maze generation algorithms and add more comprehensive unit tests to cover edge cases in the visualization module.

### Tools Used
*   **Package Management**: `uv`
*   **Building**: `hatchling`
*   **Linting & Static Analysis**: `flake8`, `mypy`
*   **Testing**: `pytest`
*   **Automation**: `make`
*   **Version Control**: `git`

## Resources

### References
* [Maze Generation: Recursive Backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking) - The primary reference used for understanding and implementing the generation logic.

* [Breadth-First Search (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search) - Reference for the pathfinding algorithm used to solve the maze.

### AI Usage
This project utilized AI assistance for the following tasks:

* **Concept Clarification**: Used AI to explain the underlying logic of the Recursive Backtracker and BFS algorithms.

* **Debugging**: Assisted in identifying and fixing errors within the bitmasking system for wall representation.

* **Code Generation**: Generated boilerplate code, specifically for the `Makefile` and project structure setup.

* **Documentation**: Used AI to outline, draft, and format this `README.md` file to ensure compliance with project requirements.