from UserFacing.Clues.Subclue import Subclue
from Utils import get_int_input

class ClueRegular():

    def __init__(self, problem):
        self.problem = problem
        self.type = "Regular"

    def set_from_user(self):
        self.initialise_subclues_from_user()
        self.set_subclues_from_user()

    def initialise_subclues_from_user(self):
        prompt = "\nHow many options are there in this clue?\n"
        self.subclue_count = get_int_input(prompt, lower_bound=1)
        self.subclues = [Subclue(self, index)
                         for index in range(self.subclue_count)]

    def set_subclues_from_user(self):
        for subclue in self.subclues:
            subclue.set_from_user()

    def __str__(self):
        string = (f"Type: {self.type}\n"
                  f"Subclue count: {self.subclue_count}")
        return string
