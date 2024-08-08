import pandas as pd


class Table():

    def __init__(self, problem):
        self.problem = problem

    def display(self, solution):
        grid = self.grid_by_element(solution)
        grid = self.get_grid_by_characteristic(grid)
        self.set_dataframe(grid)
        print(self.df.to_string())

    def grid_by_element(self, solution):
        grid = [[characteristic.property_names[index]
                 for characteristic, index in
                 zip(self.problem.characteristics, element)]
                for element_index, element in enumerate(solution)]
        return grid

    def get_grid_by_characteristic(self, grid):
        grid = {characteristic.name: row
                for characteristic, row in
                zip(self.problem.characteristics,
                    list(zip(*grid)))}
        return grid

    def set_dataframe(self, grid):
        self.df = pd.DataFrame(grid)
        self.df = self.df.set_index(self.df.columns[0])
        self.df.index.name = None
