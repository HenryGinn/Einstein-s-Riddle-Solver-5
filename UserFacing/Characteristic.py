from Utils import get_non_repeating_input

class Characteristic():

    def __init__(self, ID, problem):
        self.id = ID
        self.problem = problem
        self.name = None
        self.property_names = []

    def set_from_user(self):
        self.set_characteristic_name()
        self.set_property_names()
        pass

    def set_characteristic_name_general(self):
        prompt = "What is the name of the characteristic: "
        name = get_non_repeating_input(prompt, self.problem.characteristic_names)
        self.name = name
        self.problem.characteristic_names.append(name)

    def __str__(self):
        string = (f"Characteristic ID: {self.id}\n"
                  f"Characteristic type: {self.type}\n"
                  f"Characteristic name: {self.name}\n"
                  f"Property names:{self.get_property_name_list(indent=2)}")
        return string

    def get_property_name_list(self, indent=0):
        joining_string = "\n" + f"{indent * ' '}"
        property_names = "".join([f"{joining_string}{name}" for name in self.property_names])
        return property_names

    def get_base_data_dict(self):
        base_data_dict = {"Type": self.type,
                          "Name": self.name,
                          "Properties": self.property_names}
        return base_data_dict

    def load_from_dict(self, characteristic_dict):
        self.name = characteristic_dict["Name"]
        self.property_names = characteristic_dict["Properties"]

    def __str__(self):
        string = (f"  Type: {self.type}\n"
                  f"  Name: {self.name}\n"
                  f"  Property Names:{self.get_property_name_list(indent=4)}")
        return string
