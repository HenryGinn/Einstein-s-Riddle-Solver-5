from UserFacing.Clues.ClueRegular import ClueRegular
from UserFacing.Clues.ClueFamily import ClueFamily
from UserFacing.Clues.ClueMurder import ClueMurder
from Utils.IntInput import get_int_input
from Utils.Strings import get_list_string

class Clue():
    
    def __init__(self, problem):
        self.problem = problem

    def set_from_user(self):
        self.set_type_data()
        prompt = "\nHow many options are there in this clue?\n"
        self.subclue_count = get_int_input(prompt, lower_bound=1)
        self.subclues = [self.get_subclue_from_user(subclue_index)
                         for subclue_index in range(self.subclue_count)]

    def set_type_data(self):
        self.type_prompt = self.problem.clues_obj.clue_input.clue_type_prompt
        self.subclue_types = self.problem.clues_obj.clue_input.type_options

    def get_subclue_from_user(self, subclue_index):
        subclue_class = self.get_subclue_class()
        subclue = subclue_class(self, subclue_index)
        subclue.clue_input = self.clue_input
        subclue.set_from_user()
        return subclue

    def get_subclue_class(self):
        if len(self.subclue_types) == 1:
            subclue_class = ClueRegular
        else:
            subclue_class = self.get_subclue_class_from_choice()
        return subclue_class

    def get_subclue_class_from_choice(self):
        options_count = len(self.subclue_types)
        subclue_type_input = get_int_input(self.type_prompt, 1, options_count)
        subclue_class = self.subclue_types[subclue_type_input - 1]
        return subclue_class

    def __str__(self):
        string = (f"Subclue count: {self.subclue_count}\n"
                  f"Subclues:\n{get_list_string(self.subclues)}")
        return string
