import numpy as np
import time
import sys
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label


grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 0, 0, 0]
])

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



def astar(start, goal, grid):
    start_time = time.perf_counter()
    #print(f"Start time: {start_time}")  # Debugging print
    nodes_explored = 0

    open_set = set([start])
    closed_set = set()

    came_from = {}

    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        if current == goal:
            path = []
            while current != start:  
                path.append(current)
                current = came_from[current]
            path.append(start)  
            path.reverse()  
            end_time = time.perf_counter()
            #print(f"End time: {end_time}")  # Debugging print
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time


        open_set.remove(current)
        closed_set.add(current)
        nodes_explored += 1

        for neighbor in get_neighbors(current, grid):  
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

    end_time = time.time()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time


def branch_and_bound(start, goal, grid):
    start_time = time.perf_counter()
    nodes_explored = 0

    queue = [(start, [start])]
    visited = set()

    while queue:
        (vertex, path) = queue.pop(0)
        if vertex in visited:
            continue
        visited.add(vertex)
        nodes_explored += 1

        if vertex == goal:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return path, nodes_explored, execution_time

        for next_node in get_neighbors(vertex, grid): 
            if next_node not in visited:
                new_path = list(path)
                new_path.append(next_node)
                queue.append((next_node, new_path))

    end_time = time.time()
    execution_time = end_time - start_time
    return [], nodes_explored, execution_time


class Cell(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cell_state = 'empty'
        self.is_start = False
        self.is_goal = False

    def on_press(self):
        app = App.get_running_app()
        app.on_cell_press(self)

    def toggle_state(self):
        if self.cell_state == 'empty':
            self.cell_state = 'obstacle'
            self.background_color = (1, 0, 0, 1)
        else:
            self.reset_state()
    def reset_state(self):
        self.cell_state = 'empty'
        self.is_start = False
        self.is_goal = False
        self.background_color = (1, 1, 1, 1)

    def set_start(self):
        self.is_start = True
        self.is_goal = False
        self.cell_state = 'start'
        self.background_color = (0, 1, 0, 1)

    def set_goal(self):
        self.is_start = False
        self.is_goal = True
        self.cell_state = 'goal'
        self.background_color = (0, 0, 1, 1)

    def on_touch_down(self, touch):
    # Do nothing(if this gets changed, the app will crash on clicking on grid, SO DON"T for 100th time...)
        return

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

class PathfindingVisualizerApp(App):
    predefined_grids = {
        'Scenario 1': {'start': (0, 0), 'goal': (3, 3),
                       'grid': np.array([
                           [0, 0, 0, 0, 1],
                           [0, 1, 0, 0, 1],
                           [0, 1, 0, 1, 0],
                           [0, 0, 0, 0, 0],
                           [0, 1, 1, 1, 0]])},
                'Scenario 2': {'start': (0, 0), 'goal': (4, 4),
                             'grid': np.array([
                                 [0, 0, 0, 0, 1],
                                 [0, 1, 0, 0, 1],
                                 [0, 1, 0, 1, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 1, 1, 1, 0]])},
        'Scenario 3': {'start': (0, 0), 'goal': (4, 4),
                              'grid': np.array([
                                  [0, 0, 0, 0, 0],
                                  [0, 1, 1, 0, 1],
                                  [0, 1, 0, 0, 0],
                                  [0, 0, 0, 1, 1],
                                  [0, 1, 0, 0, 0]])},
        'Scenario 4': {'start': (0, 1), 'goal': (4, 4),
                                 'grid': np.array([
                                     [0, 1, 0, 0, 0],
                                     [0, 1, 0, 0, 0],
                                     [0, 1, 0, 0, 0],
                                     [0, 0, 0, 1, 1],
                                     [0, 0, 0, 0, 0]])},
        'Scenario 5': {'start': (0, 0), 'goal': (4, 4),
                             'grid': np.array([
                                 [0, 0, 0, 0, 0],
                                 [0, 1, 1, 1, 1],
                                 [0, 1, 0, 0, 0],
                                 [0, 1, 0, 0, 0],
                                 [0, 1, 0, 0, 0]])},
    }

    
    def build(self):
        main_layout = BoxLayout(orientation='horizontal')

        self.grid_layout = GridLayout(cols=5, rows=5, size_hint=(.7, 1))
        for y in range(5):
            for x in range(5):
                cell = Cell()
                cell.position = (x, y)
                self.grid_layout.add_widget(cell)

        side_menu = BoxLayout(orientation='vertical', size_hint=(.3, 1))

        self.grid_selector = Spinner(
            text='Select Grid',
            values=list(self.predefined_grids.keys()),
            size_hint=(1, None),
            height=44
        )
        self.grid_selector.bind(text=self.on_grid_select)

        algorithm_spinner = Spinner(
            text='Select Algorithm',
            values=('A*', 'Branch and Bound'),
            size_hint=(1, None),
            height=44
        )
        algorithm_spinner.bind(text=self.on_algorithm_select)

        run_button = Button(
            text='Run',
            size_hint=(1, None),
            height=44
        )
        run_button.bind(on_press=self.run_algorithm)

        side_menu.add_widget(self.grid_selector)
        side_menu.add_widget(algorithm_spinner)
        side_menu.add_widget(run_button)

        self.console_output = TextInput(
            readonly=True,
            size_hint=(1, 0.3),  
            background_color=(0, 0, 0, 1),  
            foreground_color=(1, 1, 1, 1),  
            font_size='16sp'  
        )

        side_menu.add_widget(self.console_output)

        sys.stdout = TextOutput(self.console_output)
        sys.stderr = TextOutput(self.console_output)

        main_layout.add_widget(self.grid_layout)
        main_layout.add_widget(side_menu)


        Window.bind(on_resize=self.on_window_resize)
        return main_layout

    def on_window_resize(self, instance, width, height):
        self.clear_path()  

    def on_grid_select(self, spinner, text):
        self.clear_path()  
        self.setup_grid(text)


    def setup_grid(self, grid_name):
            grid_info = self.predefined_grids[grid_name]
            self.start_point = grid_info['start']
            self.goal_point = grid_info['goal']
            grid_array = grid_info['grid']

            for y in range(5):
                for x in range(5):
                    cell = self.grid_layout.children[-(y * 5 + x + 1)]
                    cell.reset_state()
                    if grid_array[y][x] == 1:
                        cell.toggle_state()
                    if (x, y) == self.start_point:
                        cell.set_start()
                    if (x, y) == self.goal_point:
                        cell.set_goal()

    def get_grid_state(self):
        grid_state = [[0 for _ in range(5)] for _ in range(5)]
        for cell in self.grid_layout.children:
            x, y = cell.position
            grid_state[y][x] = 1 if cell.cell_state == 'obstacle' else 0
        return grid_state

    def clear_path(self):
        self.grid_layout.canvas.after.clear()
        self.path_instructions = []

    def display_path(self, path):
        self.path_index = 0
        self.path = path
        Clock.schedule_interval(self.animate_path, 1 / 30)  # FPS

    def animate_path(self, dt):
        if self.path_index < len(self.path):
            x, y = self.path[self.path_index]
            cell = self.grid_layout.children[-(y * 5 + x + 1)]
            with self.grid_layout.canvas.after:
                Color(0, 0, 1, mode='rgba')
                d = min(cell.width, cell.height) / 4
                self.path_instructions.append(Ellipse(pos=(cell.center_x - d / 2, cell.center_y - d / 2), size=(d, d)))
                if self.path_index > 0:
                    prev_x, prev_y = self.path[self.path_index - 1]
                    prev_cell = self.grid_layout.children[-(prev_y * 5 + prev_x + 1)]
                    self.path_instructions.append(Line(points=[prev_cell.center_x, prev_cell.center_y, cell.center_x, cell.center_y], width=1.5))
            self.path_index += 1
        else:
            Clock.unschedule(self.animate_path)


    def run_algorithm(self, instance):
        if not self.selected_algorithm:
            print("Please select an algorithm first.")
            return

        grid_state = self.get_grid_state()
        start_point = self.start_point
        goal_point = self.goal_point

        if not (0 <= start_point[0] < 5 and 0 <= start_point[1] < 5 and
                0 <= goal_point[0] < 5 and 0 <= goal_point[1] < 5):
            print("Start or goal coordinates are out of grid bounds.")
            return

        path = []  

        if self.selected_algorithm == 'A*':
            path, nodes_explored, execution_time = astar(start_point, goal_point, grid_state)
        elif self.selected_algorithm == 'Branch and Bound':
            path, nodes_explored, execution_time = branch_and_bound(start_point, goal_point, grid_state)

        if path:
            print(f"Path found: {path}")
            print(f"Nodes explored: {nodes_explored}")
            self.display_path(path)
        else:
            print("No path found.")

    def on_algorithm_select(self, spinner, text):
        self.clear_path()  
        self.selected_algorithm = text

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    
    def run_algorithm(self, instance):
        self.clear_path()
        Clock.unschedule(self.animate_path)

        if not hasattr(self, 'selected_algorithm') or self.selected_algorithm is None:
            self.show_popup("Whoops", "Please select an algorithm first.")
            return

        if not hasattr(self, 'start_point') or not hasattr(self, 'goal_point'):
            self.show_popup("Whoops", "Please select a grid first.")
            return

        grid_state = self.get_grid_state()
        start_point = self.start_point
        goal_point = self.goal_point

        if not (0 <= start_point[0] < len(grid_state) and 0 <= start_point[1] < len(grid_state[0]) and
                0 <= goal_point[0] < len(grid_state) and 0 <= goal_point[1] < len(grid_state[0])):
            print("Start or goal coordinates are out of grid bounds.")
            return

        path, nodes_explored, execution_time = [], 0, 0
        if self.selected_algorithm == 'A*':
            path, nodes_explored, execution_time = astar(start_point, goal_point, grid_state)
        elif self.selected_algorithm == 'Branch and Bound':
            path, nodes_explored, execution_time = branch_and_bound(start_point, goal_point, grid_state)

        if path:
            print(f"Path found: {path}")
            print(f"Nodes explored: {nodes_explored}")
            print(f"Execution time:\n{execution_time:.10f}")
            self.display_path(path)
        else:
            print("No path found.")

    


if __name__ == '__main__':
    app = PathfindingVisualizerApp()
    app.run()
