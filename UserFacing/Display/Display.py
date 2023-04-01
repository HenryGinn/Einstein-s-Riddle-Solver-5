import tkinter as tk

from UserFacing.Display.DisplaySettings import DisplaySettings 

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
        self.setup_window()
        self.root.mainloop()

    def setup_window(self):
        self.window_width = int(self.root.winfo_screenwidth() * self.window_width_multiplier)
        self.window_height = int(self.root.winfo_screenheight() * self.window_height_multiplier)
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.configure(bg=self.background_colour)
        
    def draw_grid_and_labels(self):
        self.set_label_names()
        #self.set_grid_size_constants()

    def set_label_names(self):
        self.set_label_names_down()
        self.set_label_names_across()

    def set_label_names_down(self):
        characteristics_down = self.problem.characteristics[:-1]
        self.label_names_down = [characteristic.display_names
                                 for characteristic in characteristics_down]

    def set_label_names_across(self):
        characteristics_across = self.problem.characteristics[:0:-1]
        self.label_names_across = [characteristic.display_names
                                   for characteristic in characteristics_across]

    def set_grid_size_constants(self):
        self.set_max_dimensions()
        self.set_cell_size()

    def set_max_dimensions(self):
        self.set_max_dimensions_labels()
        self.set_cell_counts()

    def set_max_dimensions_labels(self):
        self.labels_width = max(self.label_names_down, key=len)
        self.labels_height = max(self.label_names_across, key=len)

    def set_cell_counts(self):
        self.cell_count_horizontal = len(self.label_names_across)
        self.cell_count_vertical = len(self.label_names_down)

    def set_cell_size(self):
        cell_height = (self.window_height - 2*self.edge_of_screen_buffer_y - self.labels_height)/self.cell_count_vertical
        cell_width = (self.window_width - 2*self.edge_of_screen_buffer_y - self.labels_width)/self.cell_count_horizontal
