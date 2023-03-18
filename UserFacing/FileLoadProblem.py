import json

from UserFacing.RegularCharacteristic import RegularCharacteristic
from UserFacing.QuantitativeCharacteristic import QuantitativeCharacteristic
from UserFacing.FamilyCharacteristic import FamilyCharacteristic

class FileLoadProblem():

    def __init__(self, problem_structure):
        self.problem_structure = problem_structure
        self.problem = problem_structure.problem
        self.problem_structure_dict = {}

    def load_problem(self):
        self.create_problem_structure_dict()
        self.load_element_data()
        self.load_characteristic_data()
        self.load_murder_mystery_data()

    def create_problem_structure_dict(self):
        path = self.problem.problem_structure_path
        with open(path, "r") as file:
            self.problem_structure_dict = json.load(file)
    
    def load_element_data(self):
        self.problem.element_count = self.problem_structure_dict["Elements"]
    
    def load_characteristic_data(self):
        characteristic_dicts = self.problem_structure_dict["Characteristics"]
        self.problem.characteristics = [self.load_characteristic(characteristic_dict, index)
                                        for index, characteristic_dict in enumerate(characteristic_dicts)]

    def load_characteristic(self, characteristic_dict, index):
        characteristic_type = characteristic_dict["Type"]
        characteristic_class = self.get_characteristic_class(characteristic_type)
        characteristic_obj = characteristic_class(index, self.problem)
        characteristic_obj.load_from_dict(characteristic_dict)
        return characteristic_obj

    def get_characteristic_class(self, characteristic_type):
        characteristic_classes = self.problem_structure.get_characteristic_classes()
        characteristic_type_IDs = {"Regular": 1, "Quantitative": 2, "Family": 3}
        characteristic_type_ID = characteristic_type_IDs[characteristic_type]
        characteristic_class = characteristic_classes[characteristic_type_ID]
        return characteristic_class

    def load_murder_mystery_data(self):
        self.problem.murder_variation = self.problem_structure_dict["Murder Mystery Variation"]
    
    def __str__(self):
        string = json.dumps(self.problem_structure_dict,
                            indent=2)
        return string
