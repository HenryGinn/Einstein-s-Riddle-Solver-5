from UserFacing.Clues.Subclue import Subclue
from Utils.Input import get_options_input
from Utils.IntInput import get_int_input

class ClueRegular(Subclue):

    def __init__(self, clue, index):
        Subclue.__init__(self, clue, index)
        self.type = "Regular"
        self.set_subtype_function_dict()

    def set_subtype_function_dict(self):
        self.subtype_function_dict = {"Concrete": self.concrete_subtype,
                                      "Quantitive": self.quantitive_subtype,
                                      "Family": self.family_subtype}

    def set_from_user(self):
        subtype_input_index = self.get_subtype_input() - 1
        subtype_names = list(self.clue_input.regular_subclue_subtypes.keys())
        subtype_name = subtype_names[subtype_input_index]
        self.subtype_function_dict[subtype_name]()

    def get_subtype_input(self):
        base_prompt = "What type of regular subclue is this?"
        options = self.clue_input.regular_subclue_subtypes.values()
        subtype_input = get_options_input(base_prompt, options)
        return subtype_input
        
    def concrete_subtype(self):
        property_1, property_2 = self.get_concrete_properties()

    def get_concrete_properties(self):
        property_1 = self.clue_input.get_property(property_types=["Regular", "Quantitative"])
        property_2 = self.clue_input.get_property(previous_properties=[property_1],
                                                  property_types=["Regular", "Quantitative"])
        return property_1, property_2

    def quantitive_subtype(self):
        print("Quantitative")

    def family_subtype(self):
        print("Family")
