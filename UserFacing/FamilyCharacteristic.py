from UserFacing.Characteristic import Characteristic
from Utils import get_int_input
from Utils import get_consecutive_list
from RelationNaming import name_relation

class FamilyCharacteristic(Characteristic):

    direct_relations = ["Son", "Daughter",
                        "Mother", "Father",
                        "Brother", "Sister",
                        "Wife", "Husband"]

    def __init__(self, ID, problem):
        Characteristic.__init__(self, ID, problem)
        self.type = "Family"

    def set_characteristic_name(self):
        self.name = "Family"

    def set_property_names(self):
        self.set_family_tree_information()
        self.generate_family()
        self.filter_family()
        self.create_relation_names()
        input()

    def set_family_tree_information(self):
        self.set_in_laws()
        self.set_generations()
        self.set_spouses()
        self.set_same_sex()

    def set_in_laws(self):
        prompt = ("Are there any in-law relations?\n"
                  "1: No\n"
                  "2: Maybe\n")
        in_laws_user_input = get_int_input(prompt, 1, 2)
        self.in_laws = {1: False, 2: True}[in_laws_user_input]

    def set_generations(self):
        self.set_generations_young()
        self.set_generations_old()

    def set_generations_young(self):
        prompt = ("How many generations are below some element?\n"
                  "If you do not know, enter -1\n")
        self.generations_young = get_int_input(prompt, -1, self.problem.element_count - 1)
        self.process_generations_young()

    def process_generations_young(self):
        if self.generations_young == -1:
            self.generations_young = self.problem.element_count - 1
    
    def set_generations_old(self):
        prompt = ("How many generations are below that same element?\n"
                  "If you do not know, enter -1\n")
        self.generations_old = get_int_input(prompt, -1, self.problem.element_count - 1)
        self.process_generations_old()

    def process_generations_old(self):
        if self.generations_old == -1:
            self.generations_old = self.problem.element_count - 1

    def set_spouses(self):
        prompt = ("Are any spouses present in the family?\n"
                  "1: No\n"
                  "2: Maybe\n")
        spouses_user_input = get_int_input(prompt, 1, 2)
        self.spouses = {1: False, 2: True}[spouses_user_input]

    def set_same_sex(self):
        prompt = ("Are any same-sex relations present in the family?\n"
                  "1: No\n"
                  "2: Maybe\n")
        same_sex_user_input = get_int_input(prompt, 1, 2)
        self.same_sex = {1: False, 2: True}[same_sex_user_input]

    def generate_family(self):
        self.relations = []
        for members_left_to_add in range(1, self.problem.element_count):
            self.add_family_member(members_left_to_add, [])

    def add_family_members(self, members_left_to_add, relations):
        if members_left_to_add == 0:
            self.relations.append(relations)
        else:
            return self.add_family_member(members_left_to_add, relations)

    def add_family_member(self, members_left_to_add, relations):
        for relation in self.direct_relations:
            new_relations = relations.copy()
            new_relations.append(relation)
            self.add_family_members(members_left_to_add - 1, new_relations)
        
    def filter_family(self):
        self.relations = [relation for relation in self.relations
                          if self.is_valid_relation(relation)]

    def is_valid_relation(self, relation):
        check_functions = self.get_check_relations_functions()
        relation_valid = self.check_relation_valid(relation, check_functions)
        return relation_valid

    def get_check_relations_functions(self):
        check_functions = [self.check_pairs,
                           self.check_generations, self.check_in_laws,
                           self.check_no_spouses, self.check_same_sex]
        return check_functions

    def check_relation_valid(self, relation, check_functions):
        for check_function in check_functions:
            if check_function(relation):
                return False
        return True

    def check_pairs(self, relation):
        for pair in get_consecutive_list(relation, 2):
            if self.check_pair(pair):
                return True
        return False

    def check_pair(self, pair):
        check_pair_functions = self.get_check_pair_functions()
        for check_pair_function in check_pair_functions:
            if check_pair_function(pair):
                return True
        return False

    def get_check_pair_functions(self):
        check_functions = [self.no_sibling_pairs, self.no_spouse_pairs,
                           self.no_parent_childs, self.no_child_parents,
                           self.no_parent_spouse, self.no_child_sibling,
                           self.no_sibling_parents, self.no_spouse_child]
        return check_functions

    def no_sibling_pairs(self, pair):
        return (self.is_sibling(pair[0]) and self.is_sibling(pair[1]))

    def no_spouse_pairs(self, pair):
        return (self.is_spouse(pair[0]) and self.is_spouse(pair[1]))

    def no_parent_childs(self, pair):
        return (self.is_child(pair[0]) and self.is_parent(pair[1]))

    def no_child_parents(self, pair):
        return (self.is_parent(pair[0]) and self.is_child(pair[1]))

    def no_parent_spouse(self, pair):
        return (self.is_parent(pair[0]) and self.is_spouse(pair[1]))

    def no_child_sibling(self, pair):
        return (self.is_child(pair[0]) and self.is_sibling(pair[1]))

    def no_sibling_parents(self, pair):
        return (self.is_sibling(pair[0]) and self.is_parent(pair[1]))

    def no_spouse_child(self, pair):
        return (self.is_spouse(pair[0]) and self.is_child(pair[1]))


    def check_in_laws(self, relation):
        if self.in_laws is False:
            return ("Husband" in relation[:-1] or "Wife" in relation[:-1])
        else:
            return False

    def check_generations(self, relation):
        generations = 0
        for direct_relation in relation:
            generations = self.update_generations(generations, direct_relation)
            if self.generations_invalid(generations):
                return True
        return False

    def update_generations(self, generations, direct_relation):
        generations = self.increase_generation_if_parent(generations, direct_relation)
        generations = self.decrease_generation_if_child(generations, direct_relation)
        return generations

    def increase_generation_if_parent(self, generations, direct_relation):
        if self.is_parent(direct_relation):
            generations += 1
        return generations

    def decrease_generation_if_child(self, generations, direct_relation):
        if self.is_child(direct_relation):
            generations -= 1
        return generations

    def generations_invalid(self, generations):
        too_young = (-1*generations > self.generations_young)
        too_old = (generations > self.generations_old)
        invalid = too_young or too_old
        return invalid

    def check_no_spouses(self, relation):
        if self.spouses is False:
            return ("Husband" in relation or "Wife" in relation)
        else:
            return False

    def check_same_sex(self, relation):
        if self.same_sex is False:
            return self.no_same_sex(relation)
        else:
            return False

    def no_same_sex(self, relation):
        for pair in get_consecutive_list(relation, 2):
            if self.no_male_husbands(pair) or self.no_female_wives(pair):
                return True
        return False

    def no_male_husbands(self, pair):
        return (self.is_male(pair[0]) and pair[1] == "Husband")

    def no_female_wives(self, pair):
        return (self.is_female(pair[0]) and pair[1] == "Wife")
    

    def is_male(self, direct_relation):
        return (direct_relation in ["Brother", "Father", "Son", "Husband"])

    def is_female(self, direct_relation):
        return (direct_relation in ["Sister", "Mother", "Daughter", "Wife"])
    
    def is_parent(self, direct_relation):
        return (direct_relation in ["Father", "Mother"])

    def is_child(self, direct_relation):
        return (direct_relation in ["Son", "Daughter"])

    def is_sibling(self, direct_relation):
        return (direct_relation in ["Brother", "Sister"])

    def is_spouse(self, direct_relation):
        return (direct_relation in ["Husband", "Wife"])

    def create_relation_names(self):
        self.relations = [name_relation(relation) for relation in self.relations]
