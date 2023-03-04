import os

from Utils import get_int_input
from UserFacing.Characteristic import Characteristic
from UserFacing.RegularCharacteristic import RegularCharacteristic
from UserFacing.QuantitativeCharacteristic import QuantitativeCharacteristic
from UserFacing.FamilyCharacteristic import FamilyCharacteristic

class ProblemStructure():

    def __init__(self, problem):
        self.problem = problem
        self.path = problem.problem_structure_path
        self.problem.characteristic_names = []
        self.problem.all_property_names = []

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

    def set_element_count(self):
        prompt = "How many elements are there in the problem: "
        lower_bound = 2
        self.problem.element_count = 7
        #self.problem.element_count = get_int_input(prompt, lower_bound=lower_bound)

    def set_murder_variation(self):
        prompt = ("Is this problem in the murder mystery variation?\n"
                  "1: No\n"
                  "2: Yes\n")
        #murder_variation_input = get_int_input(prompt, 1, 2)
        self.problem.murder_variation = False
        #self.problem.murder_variation = {1: False, 2: True}[murder_variation_input]
    
    def set_characteristic_count(self):
        prompt = self.get_characteristic_count_prompt()
        self.problem.characteristic_count = 2
        #self.problem.characteristic_count = get_int_input(prompt, lower_bound=2)

    def get_characteristic_count_prompt(self):
        if self.problem.murder_variation:
            prompt = ("How many characteristics are there in the puzzle?\n"
                      "Do not include murder mystery characteristics\n")
        else:
            prompt = "How many characteristics are there in the puzzle?\n"
        return prompt

    def create_characteristic_objects(self):
        characteristic_numbers = range(self.problem.characteristic_count)
        self.problem.characteristics = [self.get_characteristic_obj(characteristic_number)
                                        for characteristic_number in characteristic_numbers]

    def get_characteristic_obj(self, characteristic_number):
        characteristic_type_ID = self.get_characteristic_type()
        characteristic_classes = self.get_characteristic_classes()
        characteristic_class = characteristic_classes[characteristic_type_ID]
        characteristic_obj = self.make_characteristic_obj(characteristic_number, characteristic_class)
        return characteristic_obj

    def get_characteristic_type(self):
        prompt = self.get_characteristic_types_prompt()
        type_input_ID = 3
        #type_input_ID = get_int_input(prompt, 1, 3)
        return type_input_ID

    def get_characteristic_types_prompt(self):
        prompt = ("What type is this characteristic?\n"
                  "1: Regular\n"
                  "2: Quantitative\n"
                  "3: Family\n")
        return prompt

    def get_characteristic_classes(self):
        characteristic_classes = {1: RegularCharacteristic,
                                  2: QuantitativeCharacteristic,
                                  3: FamilyCharacteristic}
        return characteristic_classes

    def make_characteristic_obj(self, characteristic_number, characteristic_class):
        characteristic_obj = characteristic_class(characteristic_number, self.problem)
        characteristic_obj.set_from_user()
        return characteristic_obj
