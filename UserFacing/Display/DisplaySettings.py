class DisplaySettings():

    window_size = "full"
    window_buffer_x_ratio = 0.05
    window_buffer_y_ratio = 0.05
    colour = "dark"
    font_style = "Calibri"
    text_ratio = 0.7
    
    def __init__(self, display):
        self.display = display

    def process_kwargs(self, kwargs):
        self.kwargs = kwargs
        self.process_window_size_kwargs()
        self.process_buffers_kwargs()
        self.process_colour_kwargs()
        self.process_font_kwargs()

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
            self.set_custom_buffers()
        self.set_display_window_buffers()

    def set_custom_buffers(self):
        buffers = self.kwargs["buffer"]
        if len(buffers) == 1:
            self.set_symmetric_window_buffer_ratios(buffers)
        else:
            self.set_asymmetric_buffer_ratios(buffers)

    def set_symmetric_window_buffer_ratios(self, buffer):
        self.set_window_buffer_ratio_x(buffer)
        self.set_window_buffer_ratio_y(buffer)

    def set_asymmetric_buffer_ratios(self, buffers):
        self.set_window_buffer_ratio_x(buffers[0])
        self.set_window_buffer_ratio_y(buffer[1])

    def set_window_buffer_ratio_x(self, buffer):
        if buffer < 0 or buffer > 1:
            raise ValueError(f"Buffer value needs to be between 0 and 1: {self.buffer}")
        else:
            self.window_buffer_x_ratio = buffer

    def set_window_buffer_ratio_y(self, buffer):
        if buffer < 0 or buffer > 1:
            raise ValueError(f"Buffer value needs to be between 0 and 1: {self.buffer}")
        else:
            self.window_buffer_y_ratio = buffer

    def set_display_window_buffers(self):
        self.display.window_buffer_x_ratio = self.window_buffer_x_ratio
        self.display.window_buffer_y_ratio = self.window_buffer_y_ratio
    

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

    def process_font_kwargs(self):
        self.process_font_style()
        self.process_text_ratio()

    def process_font_style(self):
        self.display.font_style = self.font_style
        if "font" in self.kwargs:
            self.display.font_style = self.kwargs["font"]

    def process_text_ratio(self):
        self.display.text_ratio = self.text_ratio
        if "text_ratio" in self.kwargs:
            self.display.text_ratio = self.kwargs["text_ratio"]
