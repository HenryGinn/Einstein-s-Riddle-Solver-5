import tkinter as tk

class Display():

    window_size = "full"
    edge_of_screen_buffer_x = 50
    edge_of_screen_buffer_y = 50
    colour = "dark"

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
        self.setup_window()
        self.draw_grid_and_labels()

    def process_kwargs(self, kwargs):
        self.process_window_size_kwargs(kwargs)
        self.process_buffers_kwargs(kwargs)
        self.process_colour_kwargs(kwargs)

    def process_window_size_kwargs(self, kwargs):
        if "size" in kwargs:
            if kwargs["size"] == "half":
                kwargs["size"] = "half_x"
            self.window_size = kwargs["size"]

    def process_buffers_kwargs(self, kwargs):
        if "buffer" in kwargs:
            self.process_symmetry_buffer(kwargs)
        elif "buffer_x" in kwargs or "buffer_y" in kwargs:
            self.process_asymmetric_buffers(kwargs)

    def process_symmetry_buffer(self, kwargs):
        self.edge_of_screen_buffer_x = kwargs["buffer"]
        self.edge_of_screen_buffer_y = kwargs["buffer"]

    def process_asymmetric_buffers(self, kwargs):
        self.process_buffer_x(kwargs)
        self.process_buffer_y(kwargs)

    def process_buffer_x(self, kwargs):
        if "buffer_x" in kwargs:
            self.edge_of_screen_buffer_x = kwargs["buffer_x"]

    def process_buffer_y(self, kwargs):
        if "buffer_y" in kwargs:
            self.edge_of_screen_buffer_y = kwargs["buffer_y"]

    def process_colour_kwargs(self, kwargs):
        if "colour" in kwargs:
            self.colour = self.kwargs["colour"]

    def setup_window(self):
        self.root = tk.Tk()
        self.set_window_size()
        self.set_colours()
        self.root.mainloop()

    def set_window_size(self):
        window_size_functions = self.get_window_size_functions()
        window_size_functions[self.window_size]()
        self.root.geometry(f"{self.window_width}x{self.window_height}")

    def get_window_size_functions(self):
        window_size_functions = {"full": self.set_window_size_full,
                                 "half_x": self.set_window_size_half_x,
                                 "half_y": self.set_window_size_half_y,
                                 "quarter": self.set_window_size_quarter}
        return window_size_functions

    def set_window_size_full(self):
        self.window_width = self.root.winfo_screenwidth()
        self.window_height = self.root.winfo_screenheight()

    def set_window_size_half_x(self):
        self.window_width = int(self.root.winfo_screenwidth() / 2)
        self.window_height = self.root.winfo_screenheight()

    def set_window_size_half_y(self):
        self.window_width = self.root.winfo_screenwidth()
        self.window_height = int(self.root.winfo_screenheight() / 2)

    def set_window_size_quarter(self):
        self.window_width = int(self.root.winfo_screenwidth() / 2)
        self.window_height = int(self.root.winfo_screenheight() / 2)

    def set_colours(self):
        set_colours_functions = self.get_set_colours_functions()
        set_colours_functions[self.colour]()

    def get_set_colours_functions(self):
        set_colours_functions = {"light": self.set_colours_light,
                                 "dark": self.set_colours_dark}
        return set_colours_functions

    def set_colours_light(self):
        background_colour = "#FFFFFF"
        self.root.configure(bg=background_colour)
        self.font_colour = "#000000"

    def set_colours_dark(self):
        background_colour = "#001325"
        self.root.configure(bg=background_colour)
        self.font_colour = "#FFFFFF"
        
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
