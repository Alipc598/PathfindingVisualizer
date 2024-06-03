from kivy.clock import Clock
import numpy as np


def get_grid_state(grid_layout):
    grid_size = 10  
    grid_state = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
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
