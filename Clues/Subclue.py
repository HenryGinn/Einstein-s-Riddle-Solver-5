class Subclue():

    def __init__(self, clue, index):
        self.parent_clue = clue
        self.index = index
        self.problem = clue.problem
        self.type = None

    def set_from_user(self):
        pass

    def __str__(self):
        string = (f"Type: {self.type}\n"
                  f"Index: {self.index}")
        return string
