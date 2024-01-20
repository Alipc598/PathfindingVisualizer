from kivy.app import App
from kivy.uix.button import Button

class Cell(Button):
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.cell_state = 'empty'  
        self.is_start = False      
        self.is_goal = False       

    def on_press(self):
        app = App.get_running_app()
        app.on_cell_press(self)

    def toggle_state(self):
        if self.cell_state == 'empty':
            self.cell_state = 'obstacle'
            self.background_color = (1, 0, 0, 1)  # Red for obstacle
        else:
            self.reset_state()

    def reset_state(self):
        self.cell_state = 'empty'
        self.is_start = False
        self.is_goal = False
        self.background_color = (1, 1, 1, 1)  # White for empty

    def set_start(self):
        self.is_start = True
        self.is_goal = False
        self.cell_state = 'start'
        self.background_color = (0, 1, 0, 1)  # Green for start

    def set_goal(self):
        self.is_start = False
        self.is_goal = True
        self.cell_state = 'goal'
        self.background_color = (0, 0, 1, 1)  # Blue for goal
        
    def on_touch_down(self, touch):
        # Do nothing(if this gets changed, the app will crash on clicking on grid, SO DON"T for 100th time...)
            return