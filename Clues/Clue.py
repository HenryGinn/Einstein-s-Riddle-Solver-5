from Utils.IntInput import get_int_input
from Utils.Strings import get_list_string

class Clue():
    
    def __init__(self, problem):
        self.problem = problem

    def set_subclue_count_from_user(self):
        prompt = "\nHow many options are there in this clue?\n"
        self.subclue_count = get_int_input(prompt, lower_bound=1)
    
    def __str__(self):
        string = (f"Subclue count: {self.subclue_count}\n"
                  f"Subclues:\n{get_list_string(self.subclues)}")
        return string
    
