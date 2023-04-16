from UserFacing.Clues.ClueRegular import ClueRegular
from UserFacing.Clues.ClueFamily import ClueFamily
from UserFacing.Clues.ClueMurder import ClueMurder
from UserFacing.Clues.Clue import Clue
from Utils.IntInput import get_int_input

class ClueInput():

    def __init__(self, problem):
        self.problem = problem
        self.set_type_options()
        self.set_clue_type_prompt()

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
        clue.set_from_user()
        return clue
