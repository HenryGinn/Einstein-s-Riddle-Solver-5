from UserFacing.Clues.Subclue import Subclue
from Utils.IntInput import get_int_input

class ClueRegular(Subclue):

    def __init__(self, problem, index):
        Subclue.__init__(self, problem, index)
        self.type = "Regular"

    def set_from_user(self):
        pass
