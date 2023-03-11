def name_relation(relation):
    if is_spouse(relation):
        name = relation[0]
    else:
        name = get_non_spouse_name(relation)
    print(f"{relation}: {name}")
    return name

def is_spouse(relation):
    return (relation in [["Husband"], ["Wife"]])

def get_non_spouse_name(relation):
    if is_direct_in_law(relation):
        base_name = get_non_direct_in_law_name(relation[1:])
        name = f"{base_name}-in-law"
    else:
        name = get_non_direct_in_law_name(relation)
    return name

def is_direct_in_law(relation):
    return is_spouse(relation[:1])

def get_non_direct_in_law_name(relation):
    spouse_indexes = get_spouse_indexes(relation)
    in_law_components = get_in_law_components(relation, spouse_indexes)
    spouses = [relation[index] for index in spouse_indexes]
    end_genders = get_end_genders(relation, spouses)
    component_names = get_component_names(in_law_components, end_genders)
    name = "-in-law's ".join(component_names)
    if is_spouse(relation[-1:]):
        name += "-in-law"
    return name

def get_spouse_indexes(relation):
    spouse_indexes = [index for index, direct_relation in enumerate(relation)
                      if direct_relation in ["Husband", "Wife"]]
    return spouse_indexes

def get_in_law_components(relation, spouse_indexes):
    if is_spouse(relation[-1:]):
        in_law_components = get_in_law_components_spouse_end(relation, spouse_indexes)
    else:
        in_law_components = get_in_law_components_no_spouse_end(relation, spouse_indexes)
    return in_law_components

def get_in_law_components_spouse_end(relation, spouse_indexes):
    left_indexes = [-1] + spouse_indexes[:-1]
    right_indexes = spouse_indexes[:]
    in_law_components = [relation[left_index + 1:right_index]
                         for left_index, right_index
                         in zip(left_indexes, right_indexes)]
    return in_law_components

def get_in_law_components_no_spouse_end(relation, spouse_indexes):
    left_indexes = [-1] + spouse_indexes[:]
    right_indexes = spouse_indexes[:] + [len(relation)]
    in_law_components = [relation[left_index + 1:right_index]
                         for left_index, right_index
                         in zip(left_indexes, right_indexes)]
    return in_law_components

def get_component_names(in_law_components, end_genders):
    blood_relations = [Blood(component, end_gender) for component, end_gender in zip(in_law_components, end_genders)]
    component_names = [blood_relation.get_name() for blood_relation in blood_relations]
    return component_names

def get_end_genders(relation, spouses):
    end_genders = [get_gender(spouse) for spouse in spouses]
    end_genders.append(get_gender(relation[-1]))
    return end_genders

def get_gender(direct_relation):
    if direct_relation in ["Brother", "Father", "Son", "Husband"]:
        return "Male"
    else:
        return "Female"

class Blood():

    def __init__(self, relations, end_gender):
        self.relations = relations
        self.end_gender = end_gender
        self.modify_last_relation_gender()
        self.set_generations_up()
        self.set_generations_down()
        self.name = None

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
            self.name = f"Grand{ending.lower()}"
        else:
            greats = self.get_greats(generations)
            self.name = f"{greats} grand{ending.lower()}"

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
