Rules:
The code must always be linted with flake8
Every method and file must have doctstrings

Goal:
Without using containers ensure the code runs correctly in python3.10+

To Do:
In the interface, _redraw() method, the self._draw_legend() call seems to overwrite the previous self.draw_maze() call to draw the grid. This error occurs in python 3.10, but not for python 3.13 for example. Make sure to fix this bug for python 3.10+