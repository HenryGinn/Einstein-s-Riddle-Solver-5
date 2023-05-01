from Clues.ClueRegular import ClueRegular
from Clues.ClueFamily import ClueFamily
from Clues.ClueMurder import ClueMurder
from Clues.Clue import Clue
from Utils.IntInput import get_int_input
from Utils.GetProperty import GetProperty

class ClueInput():

    def __init__(self, problem):
        self.problem = problem
        self.get_property = GetProperty(self.problem)
        self.set_type_options()
        self.set_clue_type_prompt()
        self.set_subclue_subtypes()

    def set_type_options(self):
        self.add_type_regular()
        self.add_type_family()
        self.add_type_murder()

    def add_type_regular(self):
        self.type_options = [self.get_subclue_class_regular]
        self.type_prompt_options = ["Regular"]
        
    def add_type_family(self):
        if self.problem.family_present:
            self.type_options.append(self.get_subclue_class_family)
            self.type_prompt_options.append("Family")
            
    def add_type_murder(self):
        if self.problem.murder_variation:
            self.type_options.append(self.get_subclue_class_murder)
            self.type_prompt_options.append("Murder Mystery")

    def set_clue_type_prompt(self):
        self.clue_type_prompt = "\nWhat type of clue do you want to add?\n"
        for type_number, clue_type_prompt in enumerate(self.type_prompt_options):
            self.clue_type_prompt += f"{type_number + 1}: {clue_type_prompt}\n"

    def set_subclue_subtypes(self):
        self.set_regular_subclue_subtypes()
        self.set_murder_subclue_subtypes()
        self.set_family_subclue_subtypes()

    def set_regular_subclue_subtypes(self):
        self.initialise_regular_subclue_subtypes()
        self.add_regular_subclue_quantitative_subtype()
        self.add_regular_subclue_family_subtype()
        self.set_regular_subtype_prompt()

    def initialise_regular_subclue_subtypes(self):
        subtype = "Relating two explicitely given properties directly"
        self.regular_subclue_subtypes = {"Concrete": subtype}

    def add_regular_subclue_quantitative_subtype(self):
        if self.problem.quantitive_characteristics_present:
            subtype = "Relating two explicitely given properties via a quantitive relation"
            self.regular_subclue_subtypes.update({"Quantitive": subtype})

    def add_regular_subclue_family_subtype(self):
        if self.problem.family_present:
            subtype = "Relating two explicitely given properties via a family relation"
            self.regular_subclue_subtypes.update({"Family": subtype})

    def set_regular_subtype_prompt(self):
        self.regular_subtype_prompt = "\nWhat type of regular clue do you want to add?\n"
        for type_number, subtype_prompt in enumerate(self.regular_subclue_subtypes):
            self.regular_subtype_prompt += f"{type_number + 1}: {subtype_prompt}\n"

    def set_murder_subclue_subtypes(self):
        self.initialise_murder_subclue_subtypes()
        self.set_murder_subtype_prompt()

    def initialise_murder_subclue_subtypes(self):
        subtype = "Relating two explicitely given properties directly"
        self.murder_subclue_subtypes = {"Concrete": subtype}
    
    def set_murder_subtype_prompt(self):
        self.murder_subtype_prompt = "\nWhat type of murder clue do you want to add?\n"
        for type_number, subtype_prompt in enumerate(self.murder_subclue_subtypes):
            self.murder_subtype_prompt += f"{type_number + 1}: {subtype_prompt}\n"

    def set_family_subclue_subtypes(self):
        self.initialise_family_subclue_subtypes()
        self.set_family_subtype_prompt()

    def initialise_family_subclue_subtypes(self):
        subtype = "Family Subtype 1"
        self.family_subclue_subtypes = {"Concrete": subtype}
    
    def set_family_subtype_prompt(self):
        self.family_subtype_prompt = "\nWhat type of family clue do you want to add?\n"
        for type_number, subtype_prompt in enumerate(self.family_subclue_subtypes):
            self.family_subtype_prompt += f"{type_number + 1}: {subtype_prompt}\n"
        

    def get_clue_from_user(self):
        clue = Clue(self.problem)
        clue.clue_input = self
        self.add_subclues(clue)
        return clue

    def add_subclues(self, clue):
        clue.set_subclue_count_from_user()
        clue.subclues = [self.get_subclue_from_user(clue, subclue_index)
                         for subclue_index in range(clue.subclue_count)]

    def get_subclue_from_user(self, clue, subclue_index):
        subclue_class = self.get_subclue_class()
        subclue = subclue_class(clue, subclue_index)
        subclue.clue_input = self
        subclue.set_from_user()
        return subclue

    def get_subclue_class(self):
        if len(self.type_options) == 1:
            subclue_class = self.get_subclue_class_regular()
        else:
            subclue_class = self.get_subclue_class_from_choice()
        return subclue_class

    def get_subclue_class_from_choice(self):
        options_count = len(self.type_options)
        subclue_type_input = get_int_input(self.clue_type_prompt, 1, options_count)
        subclue_class = self.type_options[subclue_type_input - 1]()
        return subclue_class

    def get_subclue_class_regular(self):
        options_count = len(self.regular_subtype_prompt)
        subtype_input = get_int_input(self.regular_subtype_prompt, 1, options_count)

    def get_subclue_class_quantitative(self):
        options_count = len(self.quantitative_subtype_prompt)
        subtype_input = get_int_input(self.quantitative_subtype_prompt, 1, options_count)

    def get_subclue_class_family(self):
        options_count = len(self.family_subtype_prompt)
        subtype_input = get_int_input(self.family_subtype_prompt, 1, options_count)
