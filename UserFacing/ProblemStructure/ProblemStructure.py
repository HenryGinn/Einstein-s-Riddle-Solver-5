import os

from UserFacing.ProblemStructure.RegularCharacteristic import RegularCharacteristic
from UserFacing.ProblemStructure.QuantitativeCharacteristic import QuantitativeCharacteristic
from UserFacing.ProblemStructure.FamilyCharacteristic import FamilyCharacteristic
from UserFacing.ProblemStructure.MurderCharacteristic import MurderCharacteristic
from UserFacing.ProblemStructure.FileSaveProblem import FileSaveProblem
from UserFacing.ProblemStructure.FileLoadProblem import FileLoadProblem
from Utils.IntInput import get_int_input
from Utils.Input import get_yes_no_input
from Utils.Strings import get_list_string

class ProblemStructure():

    def __init__(self, problem):
        self.initialise_problem(problem)
        self.path = problem.problem_structure_path
        self.problem.characteristic_names = []
        self.problem.all_property_names = []

    def initialise_problem(self, problem):
        self.problem = problem
        self.problem.quantitive_characteristics_present = False

    def set_problem_structure(self):
        if os.path.exists(self.path):
            self.set_problem_structure_from_file()
        else:
            self.process_problem_structure_from_user()

    def set_problem_structure_from_file(self):
        file_load = FileLoadProblem(self)
        file_load.load_problem()

    def process_problem_structure_from_user(self):
        self.set_problem_structure_from_user()
        self.save_problem_structure_to_file()

    def set_problem_structure_from_user(self):
        self.set_element_count()
        self.set_family_present()
        self.set_murder_variation()
        self.set_characteristic_count()
        self.create_characteristic_objects()

    def set_element_count(self):
        prompt = "How many elements are there in the problem: "
        lower_bound = 2
        self.problem.element_count = get_int_input(prompt, lower_bound=lower_bound)

    def set_family_present(self):
        prompt = "\nDoes this problem involve family relations?"
        family_present_input = get_yes_no_input(prompt)
        self.problem.family_present = {1: True, 2: False}[family_present_input]
        
    def set_murder_variation(self):
        prompt = "\nIs this problem in the murder mystery variation?"
        murder_variation_input = get_yes_no_input(prompt)
        self.problem.murder_variation = {1: True, 2: False}[murder_variation_input]
    
    def set_characteristic_count(self):
        prompt = self.get_characteristic_count_prompt()
        self.problem.characteristic_count = get_int_input(prompt, lower_bound=2)

    def get_characteristic_count_prompt(self):
        if self.problem.murder_variation:
            prompt = ("\nHow many characteristics are there in the puzzle?\n"
                      "Do not include murder mystery or family characteristics\n")
        else:
            prompt = "\nHow many characteristics are there in the puzzle?\n"
        return prompt

    def create_characteristic_objects(self):
        characteristic_numbers = range(self.problem.characteristic_count)
        self.problem.characteristics = [self.get_characteristic_obj(characteristic_number)
                                        for characteristic_number in characteristic_numbers]
        self.add_family_characteristic()
        self.add_murder_characteristic()

    def get_characteristic_obj(self, characteristic_number):
        characteristic_type_ID = self.get_characteristic_type()
        characteristic_classes = self.get_characteristic_classes()
        characteristic_class = characteristic_classes[characteristic_type_ID]
        characteristic_obj = self.make_characteristic_obj(characteristic_number, characteristic_class)
        return characteristic_obj

    def get_characteristic_type(self):
        prompt = self.get_characteristic_types_prompt()
        type_input_ID = get_int_input(prompt, 1, 2)
        return type_input_ID

    def get_characteristic_types_prompt(self):
        prompt = ("\nWhat type is this characteristic?\n"
                  "1: Regular\n"
                  "2: Quantitative\n")
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

    def add_family_characteristic(self):
        if self.problem.family_present:
            characteristic_number = len(self.problem.characteristics)
            family_characteristic = self.make_characteristic_obj(characteristic_number,
                                                                 FamilyCharacteristic)
            self.problem.characteristics.append(family_characteristic)

    def add_murder_characteristic(self):
        if self.problem.murder_variation:
            characteristic_number = len(self.problem.characteristics)
            murder_characteristic = self.make_characteristic_obj(characteristic_number,
                                                               MurderCharacteristic)
            self.problem.characteristics.append(murder_characteristic)

    def save_problem_structure_to_file(self):
        file_save = FileSaveProblem(self)
        file_save.save_to_file()

    def __str__(self):
        element_string = self.get_element_string()
        characteristic_string = self.get_characteristic_string()
        murder_mystery_string = self.get_murder_mystery_string()
        string = f"\n{element_string}\n{characteristic_string}\n{murder_mystery_string}\n"
        return string
    
    def get_element_string(self):
        if hasattr(self.problem, "element_count"):
            return f"Elements: {self.problem.element_count}"
        else:
            return "Elements: None"

    def get_characteristic_string(self):
        if hasattr(self.problem, "characteristics"):
            return get_list_string(self.problem.characteristics)
        else:
            return "Characteristics: None"

    def get_murder_mystery_string(self):
        if hasattr(self.problem, "murder_variation"):
            return f"Murder Variation: {self.problem.murder_variation}"
        else:
            return "Murder Variation: None"
        
