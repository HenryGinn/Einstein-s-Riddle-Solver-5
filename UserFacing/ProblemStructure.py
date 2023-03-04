import os

from Utils import get_int_input
from UserFacing.Characteristic import Characteristic

class ProblemStructure():

    def __init__(self, problem):
        self.problem = problem
        self.path = problem.problem_structure_path

    def set_problem_structure(self):
        if os.path.exists(self.path):
            self.set_problem_structure_from_file()
        else:
            self.set_problem_structure_from_user()

    def set_problem_structure_from_file(self):
        pass

    def set_problem_structure_from_user(self):
        self.set_element_count()
        self.set_murder_variation()
        self.set_characteristic_count()
        self.create_characteristic_objects()
        self.set_characteristic_data()

    def set_element_count(self):
        prompt = "How many elements are there in the problem: "
        lower_bound = 2
        self.problem.element_count = get_int_input(prompt, lower_bound=lower_bound)

    def set_murder_variation(self):
        prompt = ("Is this problem in the murder mystery variation?\n"
                  "1: No\n"
                  "2: Yes\n")
        murder_variation_input = get_int_input(prompt, 1, 2)
        self.problem.murder_variation = {1: False, 2: True}[murder_variation_input]
    
    def set_characteristic_count(self):
        prompt = self.get_characteristic_count_prompt()
        self.problem.characteristic_count = get_int_input(prompt, lower_bound=2)

    def get_characteristic_count_prompt(self):
        if self.problem.murder_variation:
            prompt = ("How many characteristics are there in the puzzle?\n"
                      "Do not include murder mystery characteristics\n")
        else:
            prompt = "How many characteristics are there in the puzzle?\n"
        return prompt

    def create_characteristic_objects(self):
        characteristic_numbers = range(self.problem.characteristic_count)
        for characteristic_number in range(self.problem.characteristic_count):
            self.problem.characteristics = [Characteristic(characteristic_number, self.problem)
                                            for characteristic_number in characteristic_numbers]

    def set_characteristic_data(self):
        self.problem.characteristic_names = []
        for characteristic in self.problem.characteristics:
            characteristic.set_from_user()
