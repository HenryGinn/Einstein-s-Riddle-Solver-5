import tkinter as tk

from UserFacing.Display.DisplaySettings import DisplaySettings
from UserFacing.Display.Grid import Grid

class Display():

    def __init__(self, problem):
        self.problem = problem
        self.window_initialised = False

    def display(self, kwargs):
        self.initialise_window(kwargs)

    def initialise_window(self, kwargs):
        if not self.window_initialised:
            self.do_initialise_window(kwargs)
            self.window_initialised = True

    def do_initialise_window(self, kwargs):
        self.process_kwargs(kwargs)
        self.create_window()
        self.draw_grid_and_labels()

    def process_kwargs(self, kwargs):
        display_settings = DisplaySettings(self)
        display_settings.process_kwargs(kwargs)
    
    def create_window(self):
        self.root = tk.Tk()
        self.set_window_sizes()
        self.setup_window()
        self.setup_canvas()

    def setup_window(self):
        self.root.title(self.problem.name)
        self.root.geometry(f"{self.window_width}x{self.window_height}-0+0")

    def set_window_sizes(self):
        self.window_width = int(self.root.winfo_screenwidth() * self.window_width_multiplier)
        self.window_height = int((self.root.winfo_screenheight() - 134) * self.window_height_multiplier)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.configure(bg=self.background_colour)
        self.canvas.pack()
        
    def draw_grid_and_labels(self):
        grid_and_labels = Grid(self)
        grid_and_labels.draw_grid_and_labels()
