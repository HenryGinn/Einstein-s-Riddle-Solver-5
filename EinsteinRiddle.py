import os
import sys

from UserFacing.ProblemStructure.ProblemStructure import ProblemStructure
from Clues.Clues import Clues
from UserFacing.Display.Display import Display

class EinsteinRiddle():

    def __init__(self, name):
        self.name = name
        self.set_paths()
        self.initialise_objects()

    def set_paths(self):
        self.repo_path = sys.path[0]
        self.parent_folder = os.path.dirname(self.repo_path)
        self.set_puzzle_folders()
        self.set_data_folders()

    def set_puzzle_folders(self):
        self.puzzle_folders = os.path.join(self.parent_folder, "Puzzle Files")
        if os.path.isdir(self.puzzle_folders) is False:
            print("Making 'Puzzle Folders' folder\n")
            os.mkdir(self.puzzle_folders)

    def set_data_folders(self):
        self.set_parent_data_folder()
        self.problem_structure_path = os.path.join(self.data_folder, "Problem Structure.json")
        self.clue_path = os.path.join(self.data_folder, "Clue Data.json")

    def set_parent_data_folder(self):
        self.data_folder = os.path.join(self.puzzle_folders, self.name)
        if os.path.isdir(self.data_folder) is False:
            print(f"Making '{self.name}' folder\n")
            os.mkdir(self.data_folder)

    def initialise_objects(self):
        self.display_obj = Display(self)

    def set_problem_structure(self):
        self.problem_structure = ProblemStructure(self)
        self.problem_structure.set_problem_structure()

    def set_clues(self):
        self.clues_obj = Clues(self)
        self.clues_obj.set_clues()

    def output_problem_structure(self):
        if hasattr(self, "problem_structure"):
            print(self.problem_structure)
        else:
            raise Exception("Run 'set_problem_structure' method before outputting problem structure")

    def output_clues(self):
        if hasattr(self, "clues_obj"):
            print(self.clues_obj)
        else:
            raise Exception("Run 'set_clues' method before outputting clues")

    def display(self, **kwargs):
        self.display_obj.display(kwargs)
