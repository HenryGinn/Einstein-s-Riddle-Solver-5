class Blood():

    """
    This class finds a name for a blood relation
    """

    def __init__(self, relations, end_gender):
        self.relations = relations
        self.set_last_gender(end_gender)
        self.set_generations()
        self.name = None

    def set_last_gender(self, end_gender):
        self.end_gender = end_gender
        if self.relations != []:
            self.modify_last_relation_gender()

    def modify_last_relation_gender(self):
        if self.end_gender == "Male":
            self.make_last_relation_male()
        else:
            self.make_last_relation_female()

    def make_last_relation_male(self):
        male_conversion = {"Sister": "Brother", "Daughter": "Son",
                           "Mother": "Father", "Wife": "Husband"}
        if self.relations[-1] in male_conversion:
            self.relations[-1] = male_conversion[self.relations[-1]]

    def make_last_relation_female(self):
        female_conversion = {"Brother": "Sister", "Son": "Daughter",
                             "Father": "Mother", "Husband": "Wife"}
        if self.relations[-1] in female_conversion:
            self.relations[-1] = female_conversion[self.relations[-1]]

    def set_generations(self):
        self.set_generations_up()
        self.set_generations_down()

    def set_generations_up(self):
        self.generations_up = sum([1 for direct_relation in self.relations
                                   if direct_relation in ["Mother", "Father",
                                                          "Brother", "Sister"]])

    def set_generations_down(self):
        self.generations_down = sum([1 for direct_relation in self.relations
                                     if direct_relation in ["Son", "Daughter",
                                                            "Brother", "Sister"]])

    def get_name(self):
        self.set_name()
        return self.name

    def set_name(self):
        if self.relations == []:
            self.name = ""
        else:
            self.set_name_non_trivial()

    def set_name_non_trivial(self):
        if self.generations_up <= 1 or self.generations_down <= 1:
            self.set_short_name()
        else:
            self.set_long_name()

    def set_short_name(self):
        if self.is_linear_relation():
            self.set_linear_name()
        else:
            self.set_non_linear_name()

    def is_linear_relation(self):
        return (self.is_n_parent() or self.is_n_child())

    def is_n_parent(self):
        return (self.generations_down == 0)

    def is_n_child(self):
        return (self.generations_up == 0)

    def set_linear_name(self):
        if self.is_n_parent():
            self.set_parent_name()
        else:
            self.set_child_name()

    def set_parent_name(self):
        if self.generations_up == 1:
            self.name = self.relations[0]
        else:
            self.set_great_name(self.generations_up, self.relations[-1])

    def set_child_name(self):
        if self.generations_down == 1:
            self.name = self.relations[0]
        else:
            self.set_great_name(self.generations_down, self.relations[-1])

    def set_great_name(self, generations, ending):
        if generations == 2:
            self.name = f"Grand{ending}"
        else:
            greats = self.get_greats(generations)
            self.name = f"{greats} grand{ending}"

    def get_greats(self, count):
        if count == 3:
            greats = "Great"
        else:
            greats = "Great" + " great" * (count - 3)
        return greats

    def set_non_linear_name(self):
        if self.is_sibling():
            self.name = self.relations[0]
        else:
            self.set_ibling_name()

    def is_sibling(self):
        return (self.generations_up == 1
                and self.generations_down == 1)

    def set_ibling_name(self):
        self.set_ibling_data()
        if self.ibling_generation == 2:
            self.name = self.ibling_end
        else:
            self.set_great_name(self.ibling_generation, self.ibling_end)

    def set_ibling_data(self):
        self.ibling_generation = max(self.generations_up, self.generations_down)
        if self.generations_up > 1:
            self.set_pibling_end()
        else:
            self.set_nibling_end()

    def set_pibling_end(self):
        if self.relations[-1] in ["Son", "Brother"]:
            self.ibling_end = "Uncle"
        elif self.relations[-1] in ["Daughter", "Sister"]:
            self.ibling_end = "Aunt"
        else:
            raise Exception("Poorly defined pibling")

    def set_nibling_end(self):
        if self.relations[-1] in ["Son", "Brother"]:
            self.ibling_end = "Nephew"
        elif self.relations[-1] in ["Daughter", "Sister"]:
            self.ibling_end = "Niece"
        else:
            raise Exception("Poorly defined nibling")

    def set_long_name(self):
        if self.generations_up > self.generations_down:
            self.set_long_name_old()
        elif self.generations_up < self.generations_down:
            self.set_long_name_young()
        else:
            self.set_cousin_name()

    def set_long_name_old(self):
        cousin_number = self.get_order_string(self.generations_down)
        removed_number = self.get_quantity_string(self.generations_up - self.generations_down)
        self.name = f"{cousin_number} cousin {removed_number} removed"

    def set_long_name_young(self):
        cousin_number = self.get_order_string(self.generations_up)
        removed_number = self.get_quantity_string(self.generations_down - self.generations_up)
        self.name = f"{cousin_number} cousin {removed_number} removed"

    def set_cousin_name(self):
        cousin_number = self.get_order_string(self.generations_up)
        if self.generations_up == 1:
            self.name = "cousin"
        else:
            self.name = f"{cousin_number} cousin"

    def get_order_string(self, number):
        order_lookup = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
                        6: "sixth", 7: "seventh", 8: "eigth", 9: "ninth"}
        if number in order_lookup:
            order = order_lookup[number]
        else:
            order = f"{number}{self.get_number_sound(number)}"
        return order

    def get_number_sound(self, number):
        number_sounds = {1: "st", 2: "nd", 3: "rd", 4: "th", 5: "th",
                         6: "st", 7: "nd", 8: "rd", 9: "th", 0: "th"}
        number_sound = number_sounds[number % 10]
        return number_sound

    def get_quantity_string(self, number):
        if number == 1:
            quantity = "once"
        elif number == 2:
            quantity = "twice"
        else:
            quantity = f"{number} times"
        return quantity
