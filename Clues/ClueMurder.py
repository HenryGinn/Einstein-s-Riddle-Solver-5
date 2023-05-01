from Clues.Subclue import Subclue
from Utils.IntInput import get_int_input

class ClueMurder(Subclue):

    def __init__(self, problem, index):
        Subclue.__init__(self, problem, index)
        self.type = "Murder"
