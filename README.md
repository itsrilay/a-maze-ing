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

* **Lint (strict)**: Check code quality with `flake8` and `mypy --strict`

```bash
make lint-strict
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
stack = [(0, 0)]

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