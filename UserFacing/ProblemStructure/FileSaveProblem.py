import json
import os

class FileSaveProblem():

    def __init__(self, problem_structure):
        self.problem_structure = problem_structure
        self.problem = problem_structure.problem
        self.problem_structure_dict = {}

    def save_to_file(self):
        self.construct_problem_structure_dict()
        with open(self.problem.problem_structure_path, "w") as file:
            json.dump(self.problem_structure_dict, file, indent=2)

    def construct_problem_structure_dict(self):
        self.set_element_data()
        self.set_characteristics_data()
        self.set_murder_mystery_data()

    def set_element_data(self):
        self.problem_structure_dict["Elements"] = self.problem.element_count

    def set_characteristics_data(self):
        characteristics_list = [characteristic_obj.get_data_dict()
                                for characteristic_obj in self.problem.characteristics
                                if characteristic_obj.type != "Murder"]
        self.problem_structure_dict["Characteristics"] = characteristics_list

    def set_murder_mystery_data(self):
        self.problem_structure_dict["Murder Mystery Variation"] = True
    
    def __str__(self):
        string = json.dumps(self.problem_structure_dict, indent=2)
        return string
