from Utils import get_consecutive_list

class Relations():
    
    direct_relations = ["Son", "Daughter",
                        "Mother", "Father",
                        "Brother", "Sister",
                        "Wife", "Husband"]

    def __init__(self, family):
        self.family = family
        self.problem = self.family.problem
        self.set_attributes_from_family_obj()

    def set_attributes_from_family_obj(self):
        self.in_laws = self.family.in_laws
        self.generations_young = self.family.generations_young
        self.generations_old = self.family.generations_old
        self.spouses = self.family.spouses
        self.same_sex = self.family.same_sex

    def set_relations(self):
        self.generate_relations()
        self.filter_relations()

    def generate_relations(self):
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
        
    def filter_relations(self):
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
