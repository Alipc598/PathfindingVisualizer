import sys
import re 
import random
import os
import webbrowser

from kivy.app import App
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.logger import Logger
Logger.setLevel('DEBUG')

from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse

from random import choice

from algorithms import astar, branch_and_bound, dijkstra, greedy_best_first_search, hierarchical_pathfinding, jump_point_search, dynamic_astar, theta_star, bfs, dfs, swarm_algorithm
from grid_components import Cell
from utilities import TextOutput, get_grid_state
from constants import predefined_grids

class MatrixColumn(Label):
    def __init__(self, **kwargs):
        super(MatrixColumn, self).__init__(**kwargs)
        self.font_size = '16sp'
        self.color = (0, 1, 0, 1)  # Green color
        self.markup = True  # Enable markup for color and styling
        self.speed = random.uniform(0.1, 0.3)  # Random speed for each column
        self.text_lines = [' '] * 57  # Empty lines at start
        Clock.schedule_interval(self.update_text, self.speed)

    def update_text(self, dt):
        if random.randint(0, 1):
            new_char = choice('01ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        else:
            new_char = ' '  # Add empty space to simulate gaps
        self.text_lines.pop(-1)  # Remove the last line
        self.text_lines.insert(0, new_char)  # Add a new line at the top
        self.text = '\n'.join(self.text_lines)  # Update the text to display

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        float_layout = FloatLayout()

        # Matrix effect layout
        matrix_layout = GridLayout(cols=20, size_hint_y=None)
        matrix_layout.bind(minimum_height=matrix_layout.setter('height'))

        for _ in range(20):
            column = MatrixColumn()
            matrix_layout.add_widget(column)

        float_layout.add_widget(matrix_layout)

        custom_texts = ['WELCOME', 'by ALI GHAEDI', 'https://github.com/Alipc598']
        for i, text in enumerate(custom_texts):
            bbox_size = (Window.width, 40)  
            label = Label(
                text='[color=ffffff]{}[/color]'.format(text),  # White
                markup=True,
                size_hint=(None, None),
                size=bbox_size,
                pos_hint={'center_x': 0.5, 'center_y': 0.6 - i * 0.1}
            )
            float_layout.add_widget(label)

        proceed_button = Button(
            text='START',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'y': 0.1}
        )
        proceed_button.bind(on_press=self.go_to_menu)
        float_layout.add_widget(proceed_button)

        self.add_widget(float_layout)

    def go_to_menu(self, instance):
        self.manager.current = 'intro'

class IntroductionScreen(Screen):
    def __init__(self, **kwargs):
        super(IntroductionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        welcome_label = Label(text="Welcome to the Pathfinding Visualizer!", size_hint=(1, 0.8))
        layout.add_widget(welcome_label)

        predefined_button = Button(text="Predefined Scenarios", size_hint=(1, 0.1))
        predefined_button.bind(on_press=self.go_to_predefined)
        layout.add_widget(predefined_button)

        manual_button = Button(text="Manual Grid", size_hint=(1, 0.1))
        manual_button.bind(on_press=self.go_to_manual)
        layout.add_widget(manual_button)

        self.add_widget(layout)

    def go_to_predefined(self, instance):
        self.manager.current = 'main'  

    def go_to_manual(self, instance):
        popup = Popup(title='Feature Under Development',
                      content=Label(text='The Manual Grid feature is currently in progress and will be available soon.'),
                      size_hint=(None, None), size=(800, 200)) 
        popup.open()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.predefined_grids = predefined_grids
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
            values=('A*', 'Branch and Bound', 'Dijkstra', 'Greedy Best First Search', 'Hierarchical Pathfinding A*', 'Jump Point Search', 'Dynamic A*', 'Theta*', 'Breadth-First Search (BFS)', 'Depth-First Search (DFS)', 'Swarm Algorithm'),
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

        save_log_button = Button(
            text='Save Log',
            size_hint=(1, None),
            height=44
        )
        save_log_button.bind(on_press=self.save_console_output)
        side_menu.add_widget(save_log_button)

        sys.stdout = TextOutput(self.console_output)
        sys.stderr = TextOutput(self.console_output)
        main_layout.add_widget(self.grid_layout)
        main_layout.add_widget(side_menu)

        self.add_widget(main_layout)

        Window.bind(on_resize=self.on_window_resize)

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
        return get_grid_state(self.grid_layout)

    def clear_path(self, *args):
        self.grid_layout.canvas.after.clear()

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
                Ellipse(pos=(cell.center_x - d / 2, cell.center_y - d / 2), size=(d, d))
                if self.path_index > 0:
                    prev_x, prev_y = self.path[self.path_index - 1]
                    prev_cell = self.grid_layout.children[-(prev_y * 5 + prev_x + 1)]
                    Line(points=[prev_cell.center_x, prev_cell.center_y, cell.center_x, cell.center_y], width=1.5)
            self.path_index += 1
        else:
            Clock.unschedule(self.animate_path)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_algorithm_select(self, spinner, text):
        self.clear_path()
        self.selected_algorithm = text

    def run_algorithm(self, instance):
        self.clear_console()  # Clear the console before running the algorithm
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

        try:
            if self.selected_algorithm == 'A*':
                path, explored_nodes, execution_time = astar(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Branch and Bound':
                path, explored_nodes, execution_time = branch_and_bound(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Dijkstra':
                path, explored_nodes, execution_time = dijkstra(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Greedy Best First Search':
                path, explored_nodes, execution_time = greedy_best_first_search(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Hierarchical Pathfinding A*':
                path, explored_nodes, execution_time = hierarchical_pathfinding(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Jump Point Search':
                path, explored_nodes, execution_time = jump_point_search(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Dynamic A*':
                path, explored_nodes, execution_time = dynamic_astar(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Theta*':
                path, explored_nodes, execution_time = theta_star(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Breadth-First Search (BFS)':
                path, explored_nodes, execution_time = bfs(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Depth-First Search (DFS)':
                path, explored_nodes, execution_time = dfs(start_point, goal_point, grid_state)
            elif self.selected_algorithm == 'Swarm Algorithm':
                path, explored_nodes, execution_time = swarm_algorithm(start_point, goal_point, grid_state)


            if path:
                print(f"Path found: {path}")
                print(f"Nodes explored: {len(explored_nodes)}")
                print(f"Execution time: {execution_time:.10f} seconds")
                self.display_explored_nodes(explored_nodes)  # Display explored nodes
                self.display_path(path)
            else:
                print("No path found.")
        except Exception as e:
            print(f"Error running algorithm: {e}")

    def display_explored_nodes(self, explored_nodes):
        for node in explored_nodes:
            x, y = node
            cell = self.grid_layout.children[-(y * 5 + x + 1)]
            with self.grid_layout.canvas.after:
                Color(1, 1, 0, mode='rgba')  # Yellow for explored nodes
                d = min(cell.width, cell.height) / 2
                Ellipse(pos=(cell.center_x - d / 2, cell.center_y - d / 2), size=(d, d))

    def save_console_output(self, instance):
        try:
            # Define the directory for console logs
            log_dir = 'Console Logs'
            
            # Create the directory if it does not exist
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # Generate the filename and full path
            scenario_name = self.grid_selector.text.replace(' ', '_')
            algorithm_name = re.sub(r'[<>:"/\\|?*]', '_', self.selected_algorithm.replace(' ', '_'))
            filename = f"{scenario_name}_{algorithm_name}.txt"
            file_path = os.path.join(log_dir, filename)
            
            # Save the console output to the specified file
            with open(file_path, 'w') as f:
                f.write(self.console_output.text)
            print(f"Console output saved to {file_path}")
        except Exception as e:
            print(f"Error saving console output: {e}")

    def clear_console(self):
        self.console_output.text = ''

class PathfindingVisualizerApp(App):
    title = 'KiviPathVis'
    predefined_grids = predefined_grids

    def build(self):
        sm = ScreenManager()
        ws = WelcomeScreen(name='welcome')
        sm.add_widget(ws)
        ms = MainScreen(name='main')
        sm.add_widget(ms)
        intro_screen = IntroductionScreen(name='intro')  
        sm.add_widget(intro_screen)
        return sm
