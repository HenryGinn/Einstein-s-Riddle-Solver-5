from UserFacing.ProblemStructure.Characteristic import Characteristic

class MurderCharacteristic(Characteristic):

    def __init__(self, ID, problem):
        Characteristic.__init__(self, ID, problem)
        self.type = "Murder"
        self.property_names = ["Alibi", "Motive", "Weapon"]

    def set_from_user(self):
        self.set_display_names()
