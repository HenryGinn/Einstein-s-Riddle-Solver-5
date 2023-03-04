from Utils import get_int_input

class Characteristic():

    def __init__(self, ID, problem):
        self.id = ID
        self.problem = problem
        self.type = None
        self.name = None
        self.property_names = []

    def set_from_user(self):
        self.set_characteristic_type()
        self.set_characteristic_name()
        self.set_property_names()
        print(self)

    def set_characteristic_type(self):
        prompt = self.get_characteristic_types_prompt()
        type_input = get_int_input(prompt, 1, 3)
        self.type = {1: "Regular", 2: "Quantitative", 3: "Family"}[type_input]

    def get_characteristic_types_prompt(self):
        prompt = ("What type is this characteristic?\n"
                  "1: Regular\n"
                  "2: Quantitative\n"
                  "3: Family\n")
        return prompt

    def set_characteristic_name(self):
        valid_characteristic_name = False
        while valid_characteristic_name is False:
            name, valid_characteristic_name = self.attempt_get_characteristic_name()
        self.accept_characteristic_name(name)

    def attempt_get_characteristic_name(self):
        prompt = "What is the name of the characteristic: "
        name_input = input(prompt)
        name_input, valid_characteristic_name = self.process_characteristic_name(name_input)
        return name_input, valid_characteristic_name

    def process_characteristic_name(self, name):
        if name in self.problem.characteristic_names:
            return self.bad_characteristic_name_input()
        else:
            return name, True

    def bad_characteristic_name_input(self):
        print(("Sorry, that name has already been used\n"
               "Here are the previously given names:\n"
               f"{'/n'.join(self.problem.characteristic_names)}\n"))
        return None, False

    def accept_characteristic_name(self, name):
        self.characteristic_name = name
        self.problem.characteristic_names.append(name)

    def set_property_names(self):
        pass

    def __str__(self):
        string = (f"Characteristic ID: {self.id}\n"
                  f"Characteristic type: {self.type}\n"
                  f"Characteristic name: {self.name}\n"
                  f"Property names: {', '.join(self.property_names)}\n")
        return string
