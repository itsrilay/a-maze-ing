install:
	uv sync

run:
	@uv run a_maze_ing.py config.txt

debug:
	@uv run python -m pdb a_maze_ing.py config.txt

clean:
	rm -rf .mypy_cache .pytest_cache
	find . -depth -path "./.venv" -prune -o -name "__pycache__" -exec rm -rf {} +

lint:
	uv run flake8 . 
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict