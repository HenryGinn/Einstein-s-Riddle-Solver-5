from UserFacing.ProblemStructure.Characteristic import Characteristic
from Utils.IntInput import get_int_input
from Utils.Input import get_non_repeating_input

class QuantitativeCharacteristic(Characteristic):

    def __init__(self, ID, problem):
        Characteristic.__init__(self, ID, problem)
        self.type = "Quantitative"
        self.problem.quantitive_characteristics_present = True
    
    def set_characteristic_name(self):
        self.set_characteristic_name_general()

    def set_property_names(self):
        print((f"Please enter the property names for the characteristic '{self.name}'\n"
               "As this is a quantitative characteristic you must enter integers"))
        for element_number in range(self.problem.element_count):
            self.set_property_name(element_number)

    def set_property_name(self, element_number):
        prompt = f"Property {element_number + 1} name: "
        get_input_function = get_int_input
        property_name = get_non_repeating_input(prompt, self.problem.all_property_names, get_input_function)
        self.property_names.append(property_name)
        self.problem.all_property_names.append(property_name)

    def get_data_dict(self):
        data_dict = self.get_base_data_dict()
        return data_dict
