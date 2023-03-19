import os

from UserFacing.Clues.ClueInput import ClueInput
from Utils import get_yes_no_input
from Utils import get_list_string

class Clues():

    def __init__(self, problem):
        self.problem = problem
        self.problem.clues = []

    def set_clues(self):
        if os.path.exists(self.problem.clue_path):
            self.set_clues_from_file()
        else:
            self.process_clues_from_user()

    def set_clues_from_file(self):
        pass

    def process_clues_from_user(self):
        while self.user_wants_to_add_clue():
            clue = self.get_clue_from_user()
            self.problem.clues.append(clue)

    def user_wants_to_add_clue(self):
        prompt = "\nDo you want to add a clue?"
        get_another_clue_input = get_yes_no_input(prompt)
        get_another_clue = {1: True, 2: False}[get_another_clue_input]
        return get_another_clue

    def get_clue_from_user(self):
        clue_input = ClueInput(self.problem)
        clue_input.set_clue()
        return clue_input.clue

    def __str__(self):
        string = f"\nOutputting data on {len(self.problem.clues)} clues:\n"
        clue_string_list = [self.get_clue_string(clue, index)
                            for index, clue in enumerate(self.problem.clues)]
        string += "\n\n".join(clue_string_list)
        return string

    def get_clue_string(self, clue, index):
        clue_data = get_list_string(str(clue), indent=2)
        string = f"Clue number {index + 1}: {clue_data}"
        return string
