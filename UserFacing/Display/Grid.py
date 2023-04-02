import tkinter as tk
from itertools import accumulate

import numpy as np

class Grid():

    font_height_width_ratio = 1.5

    def __init__(self, display):
        self.display = display
        self.problem = display.problem
        self.canvas = display.canvas
        self.inherit_window_parameters()

    def inherit_window_parameters(self):
        self.window_width = self.display.window_width
        self.window_height = self.display.window_height
        self.window_buffer_x = int(self.window_width * self.display.window_buffer_x_ratio)
        self.window_buffer_y = int(self.window_width * self.display.window_buffer_y_ratio)

    def draw_grid_and_labels(self):
        self.set_label_names()
        self.set_grid_size_constants()
        self.draw_labels()
        self.draw_grid()

    def set_label_names(self):
        self.set_label_names_down()
        self.set_label_names_across()

    def set_label_names_down(self):
        characteristics_down = self.problem.characteristics[:-1]
        self.label_names_down_groups = [characteristic.display_names
                                        for characteristic in characteristics_down]
        self.label_names_down = [label for label_group in self.label_names_down_groups
                                 for label in label_group]

    def set_label_names_across(self):
        characteristics_across = self.problem.characteristics[:0:-1]
        self.label_names_across_groups = [characteristic.display_names
                                          for characteristic in characteristics_across]
        self.label_names_across = [label for label_group in self.label_names_across_groups
                                   for label in label_group]

    def set_grid_size_constants(self):
        self.set_label_lengths()
        self.set_cell_counts()
        self.set_cell_size()
        self.set_display_sizes()
        self.set_grid_reference_coordinates()

    def set_label_lengths(self):
        self.labels_length_down = max([len(label) for label in self.label_names_down])
        self.labels_length_across = max([len(label) for label in self.label_names_across])*np.sin(self.display.text_angle*np.pi/180)

    def set_cell_counts(self):
        self.cell_count_horizontal = len(self.label_names_across)
        self.cell_count_vertical = len(self.label_names_down)

    def set_cell_size(self):
        cell_width = self.get_potential_cell_width()
        cell_height = self.get_potential_cell_height()
        self.set_slack_direction_from_cell_dimensions(cell_width, cell_height)
        self.cell_size = int(min(cell_width, cell_height))
        self.set_font_kwargs()

    def get_potential_cell_width(self):
        allocated_height = self.window_height - 2*self.window_buffer_y
        numerator = allocated_height * self.font_height_width_ratio
        denominator = self.cell_count_vertical*self.font_height_width_ratio + self.labels_length_across*self.display.text_ratio
        cell_width = numerator / denominator
        return cell_width

    def get_potential_cell_height(self):
        allocated_width = self.window_height - 2*self.window_buffer_y
        numerator = allocated_width * self.font_height_width_ratio
        denominator = self.cell_count_horizontal*self.font_height_width_ratio + self.labels_length_down*self.display.text_ratio
        cell_height = numerator / denominator
        return cell_height

    def set_slack_direction_from_cell_dimensions(self, cell_width, cell_height):
        print(cell_width, cell_height)
        if cell_width >= cell_height:
            self.slack_direction = "Horizontal"
        else:
            self.slack_direction = "Vertical"

    def set_font_kwargs(self):
        self.display.font_size = round(3 * self.display.text_ratio * self.cell_size / 4)
        self.display.font_kwargs = {"font": (self.display.font_style, self.display.font_size),
                                    "fill": self.display.colour}

    def set_display_sizes(self):
        self.set_grid_dimensions()
        self.set_label_sizes()

    def set_grid_dimensions(self):
        self.grid_width = self.cell_count_horizontal * self.cell_size
        self.grid_height = self.cell_count_vertical * self.cell_size

    def set_label_sizes(self):
        self.labels_width = self.cell_size * self.display.text_ratio * self.labels_length_down / self.font_height_width_ratio
        self.labels_height = self.cell_size * self.display.text_ratio * self.labels_length_across / self.font_height_width_ratio

    def set_grid_reference_coordinates(self):
        if self.slack_direction == "Horizontal":
            self.set_grid_reference_coordinates_horizontal()
        else:
            self.set_grid_reference_coordinates_vertical()

    def set_grid_reference_coordinates_horizontal(self):
        self.grid_reference_x = int((self.window_width + self.labels_width - self.grid_width)/2)
        self.grid_reference_y = self.window_buffer_y + self.labels_height

    def set_grid_reference_coordinates_vertical(self):
        self.grid_reference_x = self.window_buffer_x + self.labels_width
        self.grid_reference_y = int((self.window_height + self.labels_height - self.grid_height)/2)


    def draw_labels(self):
        self.draw_labels_down()
        self.draw_labels_across()

    def draw_labels_down(self):
        for index, label in enumerate(self.label_names_down):
            self.draw_label_down(index, label)

    def draw_label_down(self, index, label):
        x_position = self.grid_reference_x - int(self.cell_size / 2)
        y_position = self.grid_reference_y + int((index + 1/2) * self.cell_size)
        self.canvas.create_text(x_position, y_position, text=label,
                                anchor="e", **self.display.font_kwargs)

    def draw_labels_across(self):
        for index, label in enumerate(self.label_names_across):
            self.draw_label_across(index, label)

    def draw_label_across(self, index, label):
        x_position = self.grid_reference_x + int((index + 1/2) * self.cell_size)
        y_position = self.grid_reference_y - int(self.cell_size / 2)
        self.canvas.create_text(x_position, y_position, text=label,
                                angle=self.display.text_angle, anchor="w", **self.display.font_kwargs)

    def draw_grid(self):
        self.set_group_sizes()
        self.draw_vertical_lines()
        self.draw_horizontal_lines()

    def set_group_sizes(self):
        self.set_group_sizes_across()
        self.set_group_sizes_down()

    def set_group_sizes_across(self):
        self.group_sizes_across = [len(labels) for labels in self.label_names_across_groups]
        self.group_sizes_across_cumulative = list(accumulate(self.group_sizes_across))

    def set_group_sizes_down(self):
        self.group_sizes_down = [len(labels) for labels in self.label_names_down_groups]
        self.group_sizes_down_cumulative = list(accumulate(self.group_sizes_down))

    def draw_vertical_lines(self):
        self.create_vertical_lines_narrow()
        self.create_vertical_lines_thick()

    def create_vertical_lines_narrow(self):
        self.set_vertical_lines_narrow_data()
        for x_position, y_end in self.vertical_lines_narrow_data:
            self.draw_vertical_line_narrow(y_end, x_position)

    def set_vertical_lines_narrow_data(self):
        self.set_vertical_lines_narrow_y_ends()
        self.set_vertical_lines_narrow_x_positions()
        self.vertical_lines_narrow_data = zip(self.vertical_lines_narrow_x_positions,
                                              self.vertical_lines_narrow_y_ends)

    def set_vertical_lines_narrow_y_ends(self):
        lengths_iterable = enumerate(self.group_sizes_down_cumulative[::-1])
        y_end_indexes = self.get_y_end_indexes(lengths_iterable)
        y_ends = np.array(y_end_indexes)*self.cell_size + self.grid_reference_y
        self.vertical_lines_narrow_y_ends = y_ends

    def get_y_end_indexes(self, lengths_iterable):
        y_end_indexes = [group_size_down_cumulative
                         for index, group_size_down_cumulative in lengths_iterable
                         for _ in range(self.group_sizes_across[index] - 1)]
        return y_end_indexes

    def set_vertical_lines_narrow_x_positions(self):
        x_positions = [index for index in range(self.cell_count_horizontal)
                       if index not in [0] + self.group_sizes_across_cumulative]
        x_positions = np.array(x_positions) * self.cell_size + self.grid_reference_x
        self.vertical_lines_narrow_x_positions = x_positions

    def draw_vertical_line_narrow(self, y_end, x_position):
        self.canvas.create_line(x_position, self.grid_reference_y,
                                x_position, y_end,
                                fill=self.display.colour)

    def create_vertical_lines_thick(self):
        self.set_vertical_lines_thick_data()
        for x_position, y_end in self.vertical_lines_thick_data:
            self.draw_vertical_line_thick(x_position, y_end)

    def set_vertical_lines_thick_data(self):
        self.set_vertical_lines_thick_x_positions()
        self.set_vertical_lines_thick_y_ends()
        self.vertical_lines_thick_data = zip(self.vertical_lines_thick_x_positions,
                                             self.vertical_lines_thick_y_ends)

    def set_vertical_lines_thick_x_positions(self):
        x_positions = [0] + self.group_sizes_across_cumulative
        x_positions = np.array(x_positions) * self.cell_size + self.grid_reference_x
        self.vertical_lines_thick_x_positions = x_positions

    def set_vertical_lines_thick_y_ends(self):
        y_ends = sorted(list(set(self.vertical_lines_narrow_y_ends)), reverse=True)
        y_ends = np.concatenate(([y_ends[0]], y_ends))
        self.vertical_lines_thick_y_ends = y_ends

    def draw_vertical_line_thick(self, x_position, y_end):
        self.canvas.create_line(x_position, self.grid_reference_y,
                                x_position, y_end,
                                fill=self.display.colour, width=3)

    def draw_horizontal_lines(self):
        self.create_horizontal_lines_narrow()
        self.create_horizontal_lines_thick()

    def create_horizontal_lines_narrow(self):
        self.set_horizontal_lines_narrow_data()
        for x_end, y_position in self.horizontal_lines_narrow_data:
            self.draw_horizontal_line_narrow(x_end, y_position)

    def set_horizontal_lines_narrow_data(self):
        self.set_horizontal_lines_narrow_x_ends()
        self.set_horizontal_lines_narrow_y_positions()
        self.horizontal_lines_narrow_data = zip(self.horizontal_lines_narrow_x_ends,
                                                self.horizontal_lines_narrow_y_positions)

    def set_horizontal_lines_narrow_x_ends(self):
        lengths_iterable = enumerate(self.group_sizes_across_cumulative[::-1])
        x_end_indexes = self.get_y_end_indexes(lengths_iterable)
        x_ends = np.array(x_end_indexes)*self.cell_size + self.grid_reference_x
        self.horizontal_lines_narrow_x_ends = x_ends

    def get_x_end_indexes(self, lengths_iterable):
        x_end_indexes = [group_size_across_cumulative
                         for index, group_size_across_cumulative in lengths_iterable
                         for _ in range(self.group_sizes_down[index] - 1)]
        return x_end_indexes

    def set_horizontal_lines_narrow_y_positions(self):
        y_positions = [index for index in range(self.cell_count_vertical)
                       if index not in [0] + self.group_sizes_across_cumulative]
        y_positions = np.array(y_positions) * self.cell_size + self.grid_reference_y
        self.horizontal_lines_narrow_y_positions = y_positions

    def draw_horizontal_line_narrow(self, x_end, y_position):
        self.canvas.create_line(self.grid_reference_x, y_position,
                                x_end, y_position,
                                fill=self.display.colour)

    def create_horizontal_lines_thick(self):
        self.set_horizontal_lines_thick_data()
        for x_end, y_position in self.horizontal_lines_thick_data:
            self.draw_horizontal_line_thick(x_end, y_position)

    def set_horizontal_lines_thick_data(self):
        self.set_horizontal_lines_thick_x_ends()
        self.set_horizontal_lines_thick_y_positions()
        self.horizontal_lines_thick_data = zip(self.horizontal_lines_thick_x_ends,
                                               self.horizontal_lines_thick_y_positions)

    def set_horizontal_lines_thick_x_ends(self):
        x_ends = sorted(list(set(self.horizontal_lines_narrow_x_ends)), reverse=True)
        x_ends = np.concatenate(([x_ends[0]], x_ends))
        self.horizontal_lines_thick_x_ends = x_ends

    def set_horizontal_lines_thick_y_positions(self):
        y_positions = [0] + self.group_sizes_down_cumulative
        y_positions = np.array(y_positions) * self.cell_size + self.grid_reference_y
        self.horizontal_lines_thick_y_positions = y_positions

    def draw_horizontal_line_thick(self, x_end, y_position):
        self.canvas.create_line(self.grid_reference_x, y_position,
                                x_end, y_position,
                                fill=self.display.colour, width=3)
