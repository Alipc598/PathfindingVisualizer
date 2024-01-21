from kivy.clock import Clock
import numpy as np

def heuristic(a, b):
    return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])

def get_neighbors(node, grid):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    neighbors = []
    x, y = node
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[ny][nx] == 0:  
                neighbors.append((nx, ny))
    return neighbors

def get_grid_state(grid_layout):
    grid_state = [[0 for _ in range(5)] for _ in range(5)]
    for cell in grid_layout.children:
        x, y = cell.position
        grid_state[y][x] = 1 if cell.cell_state == 'obstacle' else 0
    return grid_state

class TextOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        def append_text(*args):
            self.text_widget.text += text
            self.text_widget.cursor = (0, len(self.text_widget.text)) 

        Clock.schedule_once(append_text)

    def flush(self):
        pass
