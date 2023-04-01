class DisplaySettings():

    window_size = "full"
    edge_of_screen_buffer_x = 50
    edge_of_screen_buffer_y = 50
    colour = "dark"
    
    def __init__(self, display):
        self.display = display

    def process_kwargs(self, kwargs):
        self.kwargs = kwargs
        self.process_window_size_kwargs()
        self.process_buffers_kwargs()
        self.process_colour_kwargs()

    def process_window_size_kwargs(self):
        if "size" in self.kwargs:
            if self.kwargs["size"] == "half":
                self.kwargs["size"] = "half_x"
            self.window_size = self.kwargs["size"]
        self.set_window_size()

    def set_window_size(self):
        window_size_functions = self.get_window_size_functions()
        window_size_functions[self.window_size]()

    def get_window_size_functions(self):
        window_size_functions = {"full": self.set_window_size_full,
                                 "half_x": self.set_window_size_half_x,
                                 "half_y": self.set_window_size_half_y,
                                 "quarter": self.set_window_size_quarter}
        return window_size_functions

    def set_window_size_full(self):
        self.display.window_width_multiplier = 1
        self.display.window_height_multiplier = 1

    def set_window_size_half_x(self):
        self.display.window_width_multiplier = 1/2
        self.display.window_height_multiplier = 1

    def set_window_size_half_y(self):
        self.display.window_width_multiplier = 1
        self.display.window_height_multiplier = 1/2

    def set_window_size_quarter(self):
        self.display.window_width_multiplier = 1/2
        self.display.window_height_multiplier = 1/2
    

    def process_buffers_kwargs(self):
        if "buffer" in self.kwargs:
            self.process_symmetry_buffer()
        elif "buffer_x" in self.kwargs or "buffer_y" in self.kwargs:
            self.process_asymmetric_buffers()

    def process_symmetry_buffer(self):
        self.display.edge_of_screen_buffer_x = self.kwargs["buffer"]
        self.display.edge_of_screen_buffer_y = self.kwargs["buffer"]

    def process_asymmetric_buffers(self):
        self.process_buffer_x()
        self.process_buffer_y()

    def process_buffer_x(self):
        if "buffer_x" in self.kwargs:
            self.display.edge_of_screen_buffer_x = self.kwargs["buffer_x"]

    def process_buffer_y(self):
        if "buffer_y" in self.kwargs:
            self.display.edge_of_screen_buffer_y = self.kwargs["buffer_y"]
    

    def process_colour_kwargs(self):
        if "colour" in self.kwargs:
            self.colour = self.kwargs["colour"]
        self.set_colours()

    def set_colours(self):
        set_colours_functions = self.get_set_colours_functions()
        set_colours_functions[self.colour]()

    def get_set_colours_functions(self):
        set_colours_functions = {"light": self.set_colours_light,
                                 "dark": self.set_colours_dark}
        return set_colours_functions

    def set_colours_light(self):
        self.display.background_colour = "#FFFFFF"
        self.display.font_colour = "#000000"

    def set_colours_dark(self):
        self.display.background_colour = "#001325"
        self.display.font_colour = "#FFFFFF"
