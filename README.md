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

### Generation: Recurvise Backtracker
This project utilizes the **Recursive Backtracker** algorithm, a randomized implementation of Depth-First Search (DFS).

* **Mechanism**: The algorithm acts as a "miner" that carves passages by moving to random unvisited neighbors. It utilizes a stack to track the current path; when the miner reaches a dead end, it backtracks (pops from the stack) until a new unvisited neighbor is found.

* **Properties**: This approach generates "perfect" mazes, which are mathematically equivalent to spanning trees (graphs with no loops and a unique path between any two nodes).

* **Aesthetic**: The Recursive Backtracker is known for creating mazes with long, winding corridors and high complexity, making them challenging to solve manually.

### Solving: Breadth-First Search
To solve the maze, the program implements the **Breadth-First Search (BFS)** algorithm.

* **Mechanism**: BFS explores the maze layer by layer, expanding equally in all directions from the starting point. It uses a queue to manage the frontier of visited cells.

* **Optimality**: Because the maze is an unweighted grid (every step costs the same), BFS is mathematically guaranteed to find the shortest possible path from the entrance to the exit.

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