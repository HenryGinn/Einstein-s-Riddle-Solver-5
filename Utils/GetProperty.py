from Utils.Input import bad_user_input
from Utils.Strings import capitalise

class GetProperty():

    def __init__(self, problem):
        self.problem = problem
        self.set_characteristic_lookup()

    def set_characteristic_lookup(self):
        self.characteristic_lookup = {str(property_name): characteristic
                                      for characteristic in self.problem.characteristics
                                      for property_name in characteristic.property_names}

    def __call__(self, previous_properties=None,
                 previous_characteristics=None,
                 property_types=None):
        self.set_previous_properties(previous_properties)
        self.set_previous_characteristics(previous_characteristics)
        self.set_property_types(property_types)
        return self.get_property(*args, **kwargs)

    def get_property(self, previous_properties,
                     previous_characteristics,
                     property_types):
        property_name = self.do_get_property()
        return property_name

    def set_previous_properties(self, previous_properties):
        if previous_properties is None:
            self.previous_properties = []
        else:
            self.previous_properties = previous_properties

    def set_previous_characteristics(self, previous_characteristics):
        if previous_characteristics is None:
            self.previous_characteristics = []
        else:
            self.previous_characteristics = previous_characteristics            

    def set_property_types(self, property_types):
        if property_types is None:
            self.property_types = ["Regular", "Quantitative", "Family"]
        else:
            self.property_types = property_types

    def do_get_property(self):
        property_valid = False
        while not property_valid:
            property_valid, property_name = self.attempt_get_property()
        return property_name

    def attempt_get_property(self):
        prompt = "Please enter the name of a property: "
        property_name = capitalise(str(input(prompt)))
        property_valid = self.get_property_valid(property_name)
        return property_valid, property_name

    def get_property_valid(self, property_name):
        if property_name not in self.previous_properties:
            return self.property_name_unused(property_name)
        else:
            return bad_user_input(self.previous_properties)[1]    

    def property_name_unused(self, property_name):
        if property_name in self.characteristic_lookup:
            return self.property_name_exists(property_name)
        else:
            print(f"Sorry, '{property_name}' is not an existing property name")
            return False

    def property_name_exists(self, property_name):
        if self.characteristic_lookup[property_name].type in self.property_types:
            return self.property_is_valid_type(property_name)
        else:
            print(f"Sorry, you must enter a property of type {self.property_types}")
            return False

    def property_is_valid_type(self, property_name):
        if self.characteristic_lookup[property_name].name not in self.previous_characteristics:
            return True
        else:
            return bad_user_input(self.previous_characteristics)[1]
