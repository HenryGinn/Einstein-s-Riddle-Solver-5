from UserFacing.Clues.ClueRegular import ClueRegular
from UserFacing.Clues.ClueFamily import ClueFamily
from UserFacing.Clues.ClueMurder import ClueMurder
from Utils import get_int_input

class ClueInput():

    def __init__(self, problem):
        self.problem = problem

    def set_clue(self):
        self.set_clue_type()

    def set_clue_type(self):
        self.set_type_options()
        self.process_clue_type_options()

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

    def process_clue_type_options(self):
        if len(self.type_options) == 1:
            self.clue = ClueRegular(self)
        else:
            self.ask_clue_type()

    def ask_clue_type(self):
        self.set_clue_type_prompt()
        clue_class = self.get_clue_class()
        self.clue = clue_class(self)

    def get_clue_class(self):
        options_count = len(self.type_options)
        clue_type_input = get_int_input(self.clue_type_prompt, 1, options_count)
        clue_class = self.type_options[clue_type_input - 1]
        return clue_class
