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

    def set_characteristic_name_general(self):
        prompt = "What is the name of the characteristic: "
        name = get_non_repeating_input(prompt, self.problem.characteristic_names)
        self.name = name
        self.problem.characteristic_names.append(name)

    def __str__(self):
        string = (f"Characteristic ID: {self.id}\n"
                  f"Characteristic type: {self.type}\n"
                  f"Characteristic name: {self.name}\n"
                  f"Property names:\n{self.get_property_name_list()}")
        return string

    def get_property_name_list(self):
        property_names = [str(name) for name in self.property_names]
        property_names = "\n".join(property_names)
        return property_names
