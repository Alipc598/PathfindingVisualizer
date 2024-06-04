import sys
import re 
import random
import os
import webbrowser

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.uix.dropdown import DropDown


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

        welcome_label = Label(text="Welcome to the Pathfinding Visualizer!", size_hint=(1, 0.1), font_size='20sp')
        layout.add_widget(welcome_label)

        explanation_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6), padding=10, spacing=10)

        info_label = Label(
            text="This visualizer uses various algorithms to find the shortest path between two points.\n"
                 "The key concepts are:\n"
                 "[color=00ff00]g[/color]: Cost from start to current node.\n"
                 "[color=ff0000]h[/color]: Heuristic - estimated cost from current node to goal.\n"
                 "[color=0000ff]f[/color]: Total cost of the node ([color=00ff00]f = g + h[/color]).",
            size_hint=(0.5, 1),
            halign='left',
            valign='top',
            markup=True
        )
        info_label.bind(size=info_label.setter('text_size'))
        explanation_layout.add_widget(info_label)

        map_info_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), padding=10, spacing=10)

        map_info_label = Label(
            text="Map Color Coding:",
            size_hint=(1, 0.1),
            halign='left',
            valign='top',
            font_size='18sp'
        )
        map_info_label.bind(size=map_info_label.setter('text_size'))
        map_info_layout.add_widget(map_info_label)

        colors = [
            ("Obstacle", (1, 0, 0, 1)),
            ("Start Point", (0, 1, 0, 1)),
            ("Destination", (0, 0, 0.5, 1)),
            ("Explored Node", (1, 1, 0, 1)),
            ("Path", (0, 0, 1, 1))
        ]

        for text, color in colors:
            color_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=5, spacing=5)
            color_label = Label(
                text=text,
                size_hint=(0.8, 1),
                halign='left',
                valign='middle',
                font_size='16sp'
            )
            color_label.bind(size=color_label.setter('text_size'))
            color_circle = Button(
                background_normal='',
                background_color=color,
                size_hint=(0.2, 1)
            )
            color_layout.add_widget(color_label)
            color_layout.add_widget(color_circle)
            map_info_layout.add_widget(color_layout)

        explanation_layout.add_widget(map_info_layout)
        layout.add_widget(explanation_layout)

        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), padding=10, spacing=10)

        online_link_button = Button(text="Prerequisite Knowledge", size_hint=(1, 0.1))
        online_link_button.bind(on_press=self.open_online_link)
        button_layout.add_widget(online_link_button)

        # Add the educational videos button
        edu_videos_button = Button(text="Educational Videos", size_hint=(1, 0.1))
        edu_videos_button.bind(on_press=self.open_edu_videos)
        button_layout.add_widget(edu_videos_button)

        predefined_button = Button(text="Predefined Scenarios", size_hint=(1, 0.1))
        predefined_button.bind(on_press=self.go_to_predefined)
        button_layout.add_widget(predefined_button)

        manual_button = Button(text="Manual Grid", size_hint=(1, 0.1))
        manual_button.bind(on_press=self.go_to_manual)
        button_layout.add_widget(manual_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)

    def go_to_predefined(self, instance):
        self.manager.current = 'main'

    def go_to_manual(self, instance):
        manual_screen = ManualGridScreen(name='manual_grid')
        self.manager.add_widget(manual_screen)
        self.manager.current = 'manual_grid'

    def open_online_link(self, instance):
        webbrowser.open("https://www.redblobgames.com/pathfinding/a-star/introduction.html")

    def open_edu_videos(self, instance):
        dropdown = DropDown()
        youtube_links = {
            "A*": "https://www.youtube.com/watch?v=JtiK0DOeI4A",
            "Branch and Bound": "https://www.youtube.com/watch?v=3RBNPc0_Q6g",
            "Dijkstra": "https://www.youtube.com/watch?v=GazC3A4OQTE",
            "Greedy Best First Search": "https://www.youtube.com/watch?v=dv1m3L6QXWs",
            "Hierarchical Pathfinding A*": "https://www.youtube.com/watch?v=zrX-67WkK6Y",
            "Jump Point Search": "https://www.youtube.com/watch?v=__ZLnTwYNPk",
            "Dynamic A*": "https://www.youtube.com/watch?v=JtiK0DOeI4A",
            "Theta*": "https://www.youtube.com/watch?v=mAaYVTedqPQ",
            "Breadth-First Search (BFS)": "https://www.youtube.com/watch?v=oDqjPvD54Ss",
            "Depth-First Search (DFS)": "https://www.youtube.com/watch?v=7fujbpJ0LB4",
            "Swarm Algorithm": "https://www.youtube.com/watch?v=SMq-dy8Hx-Y"
        }

        for title, url in youtube_links.items():
            btn = Button(text=title, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        mainbutton = Button(text='Select Algorithm', size_hint=(1, None), height=44)
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: self.open_youtube_link(youtube_links[x]))

        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(mainbutton)

        popup = Popup(title='Educational Videos', content=popup_layout, size_hint=(None, None), size=(600, 200))
        popup.open()

    def open_youtube_link(self, url):
        webbrowser.open(url)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.predefined_grids = predefined_grids
        main_layout = BoxLayout(orientation='horizontal')

        self.grid_layout = GridLayout(cols=10, rows=10, size_hint=(.7, 1))   #Grid size
        for y in range(10):
            for x in range(10):
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

        self.console_output = TextInput(
            readonly=True,
            size_hint=(1, 0.3),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            font_size='16sp'
        )

        save_log_button = Button(
            text='Save Log',
            size_hint=(1, None),
            height=44
        )
        save_log_button.bind(on_press=self.save_console_output)

        back_button = Button(
            text='Back',
            size_hint=(1, None),
            height=44
        )
        back_button.bind(on_press=self.go_to_intro)

        side_menu.add_widget(self.grid_selector)
        side_menu.add_widget(algorithm_spinner)
        side_menu.add_widget(run_button)
        side_menu.add_widget(self.console_output)
        side_menu.add_widget(save_log_button)
        side_menu.add_widget(back_button)

        sys.stdout = TextOutput(self.console_output)
        sys.stderr = TextOutput(self.console_output)
        main_layout.add_widget(self.grid_layout)
        main_layout.add_widget(side_menu)

        self.add_widget(main_layout)

        Window.bind(on_resize=self.on_window_resize)

    def on_touch_down(self, touch):
        if self.grid_layout.collide_point(*touch.pos):
            # Touch is within the grid, disable left and right clicks
            if touch.button == 'left' or touch.button == 'right':
                return True  # Consume the touch event
        return super(MainScreen, self).on_touch_down(touch)

    def go_to_intro(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'intro'

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

        for y in range(10): #Grid size
            for x in range(10):
                cell = self.grid_layout.children[-(y * 10 + x + 1)]
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
            cell = self.grid_layout.children[-(y * 10 + x + 1)] #Grid size
            with self.grid_layout.canvas.after:
                Color(0, 0, 1, mode='rgba')
                d = min(cell.width, cell.height) / 4
                Ellipse(pos=(cell.center_x - d / 2, cell.center_y - d / 2), size=(d, d))
                if self.path_index > 0:
                    prev_x, prev_y = self.path[self.path_index - 1]
                    prev_cell = self.grid_layout.children[-(prev_y * 10 + prev_x + 1)] #Grid size
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

        try:
            grid_state = self.get_grid_state()
            start_point = self.start_point
            goal_point = self.goal_point

            if not (0 <= start_point[0] < len(grid_state) and 0 <= start_point[1] < len(grid_state[0]) and
                    0 <= goal_point[0] < len(grid_state) and 0 <= goal_point[1] < len(grid_state[0])):
                print("Start or goal coordinates are out of grid bounds.")
                return

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
            else:
                print("Unknown algorithm selected.")
                return

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
            import traceback
            traceback.print_exc()
            self.show_popup("Error", f"An error occurred while running the algorithm:\n{e}")

    def display_explored_nodes(self, explored_nodes):
        for node in explored_nodes:
            x, y = node
            cell = self.grid_layout.children[-(y * 10 + x + 1)] #Grid size
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

class ManualGridScreen(Screen):
    def __init__(self, **kwargs):
        super(ManualGridScreen, self).__init__(**kwargs)

        self.mode = 'start'  # Initialize mode

        self.grid_layout = GridLayout(cols=10, rows=10, size_hint=(.7, 1))

        for y in range(10):
            for x in range(10):
                cell = Cell()
                cell.position = (x, y)
                self.grid_layout.add_widget(cell)

        side_menu = BoxLayout(orientation='vertical', size_hint=(.3, 1))

        mode_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44)
        start_button = Button(text='Start', size_hint=(1, None), height=44, background_color=(0, 1, 0, 1))
        start_button.bind(on_press=lambda x: self.set_mode('start'))
        goal_button = Button(text='Goal', size_hint=(1, None), height=44, background_color=(0, 0, 1, 1))
        goal_button.bind(on_press=lambda x: self.set_mode('goal'))
        obstacle_button = Button(text='Obstacle', size_hint=(1, None), height=44, background_color=(1, 0, 0, 1))
        obstacle_button.bind(on_press=lambda x: self.set_mode('obstacle'))
        reset_button = Button(text='Reset Grid', size_hint=(1, None), height=44)
        reset_button.bind(on_press=self.reset_grid)

        mode_layout.add_widget(start_button)
        mode_layout.add_widget(goal_button)
        mode_layout.add_widget(obstacle_button)
        side_menu.add_widget(mode_layout)
        side_menu.add_widget(reset_button)

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

        self.console_output = TextInput(
            readonly=True,
            size_hint=(1, 0.3),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            font_size='16sp'
        )

        save_log_button = Button(
            text='Save Log',
            size_hint=(1, None),
            height=44
        )
        save_log_button.bind(on_press=self.save_console_output)

        back_button = Button(
            text='Back',
            size_hint=(1, None),
            height=44
        )
        back_button.bind(on_press=self.go_to_intro)

        side_menu.add_widget(algorithm_spinner)
        side_menu.add_widget(run_button)
        side_menu.add_widget(self.console_output)
        side_menu.add_widget(save_log_button)
        side_menu.add_widget(back_button)

        sys.stdout = TextOutput(self.console_output)
        sys.stderr = TextOutput(self.console_output)
        main_layout = BoxLayout(orientation='horizontal')
        main_layout.add_widget(self.grid_layout)
        main_layout.add_widget(side_menu)

        self.add_widget(main_layout)

        Window.bind(on_resize=self.on_window_resize)

    def set_mode(self, mode):
        self.mode = mode

    def reset_grid(self, instance):
        for cell in self.grid_layout.children:
            cell.reset_state()

    def go_to_intro(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'intro'
        Clock.schedule_once(self.remove_self, 0.1)

    def remove_self(self, dt):
        self.manager.remove_widget(self)

    def on_window_resize(self, instance, width, height):
        self.grid_layout.canvas.after.clear()

    def on_algorithm_select(self, spinner, text):
        self.clear_path()
        self.selected_algorithm = text

    def on_manual_cell_press(self, cell):
        if self.mode == 'start':
            for c in self.grid_layout.children:
                if c.is_start:
                    c.reset_state()
            cell.set_start()
        elif self.mode == 'goal':
            for c in self.grid_layout.children:
                if c.is_goal:
                    c.reset_state()
            cell.set_goal()
        elif self.mode == 'obstacle':
            cell.toggle_state()

    def run_algorithm(self, instance):
        # Implement the algorithm running logic here
        pass

    def display_explored_nodes(self, explored_nodes):
        for node in explored_nodes:
            x, y = node
            cell = self.grid_layout.children[-(y * 10 + x + 1)]
            with self.grid_layout.canvas.after:
                Color(1, 1, 0, mode='rgba')  # Yellow for explored nodes
                d = min(cell.width, cell.height) / 2
                Ellipse(pos=(cell.center_x - d / 2, cell.center_y - d / 2), size=(d, d))

    def save_console_output(self, instance):
        # Implement the logic to save console output here
        pass

    def clear_console(self):
        self.console_output.text = ''

    def clear_path(self):
        self.grid_layout.canvas.after.clear()


class PathfindingVisualizerApp(App):
    title = 'KiviPathVis'

    def build(self):
        sm = ScreenManager()

        ws = WelcomeScreen(name='welcome')
        sm.add_widget(ws)

        ms = MainScreen(name='main')
        sm.add_widget(ms)

        intro_screen = IntroductionScreen(name='intro')
        sm.add_widget(intro_screen)

        return sm

    def on_manual_cell_press(self, cell):
        screen = self.root.get_screen('manual_grid')
        screen.on_manual_cell_press(cell)

if __name__ == "__main__":
    PathfindingVisualizerApp().run()
