from UserFacing.Clues.ClueRegular import ClueRegular
from UserFacing.Clues.ClueFamily import ClueFamily
from UserFacing.Clues.ClueMurder import ClueMurder
from UserFacing.Clues.Clue import Clue
from Utils.IntInput import get_int_input
from Utils.Input import get_property

class ClueInput():

    def __init__(self, problem):
        self.problem = problem
        self.set_type_options()
        self.set_clue_type_prompt()
        self.set_subclue_subtypes()
        self.set_characteristic_lookup()

    def set_type_options(self):
        self.add_type_regular()
        self.add_type_family()
        self.add_type_murder()

    def add_type_regular(self):
        self.type_options = [ClueRegular]
        self.type_prompt_options = ["Regular"]
        
    def add_type_family(self):
        if self.problem.family_present:
            self.type_options.append(ClueFamily)
            self.type_prompt_options.append("Family")
            
    def add_type_murder(self):
        if self.problem.murder_variation:
            self.type_options.append(ClueMurder)
            self.type_prompt_options.append("Murder Mystery")

    def set_clue_type_prompt(self):
        self.clue_type_prompt = "\nWhat type of clue do you want to add?\n"
        for type_number, clue_type_prompt in enumerate(self.type_prompt_options):
            self.clue_type_prompt += f"{type_number + 1}: {clue_type_prompt}\n"

    def get_clue_from_user(self):
        clue = Clue(self.problem)
        clue.clue_input = self
        clue.set_from_user()
        return clue
    

    def set_subclue_subtypes(self):
        self.set_regular_subclue_subtypes()

    def set_regular_subclue_subtypes(self):
        self.initialise_regular_subclue_subtypes()
        self.add_regular_subclue_family_subtype()
        self.add_regular_subclue_family_subtype()

    def initialise_regular_subclue_subtypes(self):
        subtype = "Relating two explicitely given properties directly"
        self.regular_subclue_subtypes = {"Concrete": subtype}

    def add_regular_subclue_quantitive_subtype(self):
        if self.problem.quantitive_characteristics_present():
            subtype = "Relating two explicitely given properties via a quantitive relation"
            self.regular_subclue_subtypes.update({"Quantitive": subtype})

    def add_regular_subclue_family_subtype(self):
        if self.problem.family_present:
            subtype = "Relating two explicitely given properties via a family relation"
            self.regular_subclue_subtypes.update({"Family": subtype})

    def get_property(self, previous_properties=None, property_types=None):
        property_name = get_property(self.characteristic_lookup,
                                     previous_properties,
                                     property_types)
        return property_name

    def set_characteristic_lookup(self):
        self.characteristic_lookup = {str(property_name): characteristic
                                      for characteristic in self.problem.characteristics
                                      for property_name in characteristic.property_names}
