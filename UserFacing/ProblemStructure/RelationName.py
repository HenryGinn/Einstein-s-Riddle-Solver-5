from UserFacing.ProblemStructure.Blood import Blood

class RelationName():

    def __init__(self, relation):
        self.relation = relation
        self.set_relation_name()

    def set_relation_name(self):
        self.set_raw_name()
        self.fix_capitalisation()

    def set_raw_name(self):
        if self.is_spouse(self.relation[0]):
            self.starts_with_spouse()
        else:
            self.starts_with_non_spouse()

    def starts_with_spouse(self):
        if self.is_spouse(self.relation[-1]):
            self.starts_and_ends_with_spouse()
        else:
            self.only_starts_with_spouse()

    def starts_and_ends_with_spouse(self):
        if len(self.relation) == 1:
            self.name = self.relation[0]
        else:
            self.starts_and_ends_with_spouse_non_trivial()

    def starts_and_ends_with_spouse_non_trivial(self):
        self.filter_starting_spouse()
        component_names = self.get_component_names()
        self.name = "-in-law's ".join(component_names[:-1])
        self.name = f"{self.starting_spouse}'s {self.name}-in-law"

    def only_starts_with_spouse(self):
        if self.multiple_spouses():
            self.only_starts_with_spouse_multiple()
        else:
            self.only_starts_with_spouse_single()

    def only_starts_with_spouse_multiple(self):
        self.filter_starting_spouse()
        component_names = self.get_component_names()
        self.name = "-in-law's ".join(component_names)
        self.name = f"{self.starting_spouse}'s {self.name}"

    def only_starts_with_spouse_single(self):
        self.filter_starting_spouse()
        component_names = self.get_component_names()
        self.name = "-in-law's ".join(component_names)
        self.name = f"{self.name}-in-law"

    def starts_with_non_spouse(self):
        if self.is_spouse(self.relation[-1]):
            self.only_ends_with_spouse()
        else:
            self.starts_and_ends_without_spouse()

    def only_ends_with_spouse(self):
        component_names = self.get_component_names()
        self.name = "-in-law's ".join(component_names[:-1])
        self.name = f"{self.name}-in-law"

    def starts_and_ends_without_spouse(self):
        component_names = self.get_component_names()
        self.name = "-in-law's ".join(component_names)

    def is_spouse(self, direct_relation):
        return (direct_relation in ["Husband", "Wife"])

    def multiple_spouses(self):
        spouse_count = self.relation.count("Husband") + self.relation.count("Wife")
        return (spouse_count > 1)

    def filter_starting_spouse(self):
        self.starting_spouse = self.relation[0]
        self.relation = self.relation[1:]

    def set_spouse_indexes(self):
        self.spouse_indexes = [index for index, direct_relation in enumerate(self.relation)
                               if direct_relation in ["Husband", "Wife"]]

    def set_in_law_components(self):
        left_indexes = [-1] + self.spouse_indexes[:]
        right_indexes = self.spouse_indexes[:] + [len(self.relation)]
        self.in_law_components = [self.relation[left_index + 1:right_index]
                                  for left_index, right_index
                                  in zip(left_indexes, right_indexes)]

    def get_component_names(self):
        self.setup_relation_data()
        blood_relations = [Blood(component, end_gender)
                           for component, end_gender in zip(self.in_law_components, self.end_genders)]
        component_names = [blood_relation.get_name() for blood_relation in blood_relations]
        return component_names

    def setup_relation_data(self):
        self.set_spouse_indexes()
        self.set_in_law_components()
        self.set_component_end_genders()

    def set_component_end_genders(self):
        spouses = [self.relation[index] for index in self.spouse_indexes]
        self.end_genders = [self.get_gender(spouse) for spouse in spouses]
        self.end_genders.append(self.get_gender(self.relation[-1]))

    def get_gender(self, direct_relation):
        if direct_relation in ["Brother", "Father", "Son", "Husband"]:
            return "Male"
        else:
            return "Female"

    def fix_capitalisation(self):
        first_letter = self.name[0].upper()
        rest_of_name = self.name[1:].lower().strip()
        self.name = f"{first_letter}{rest_of_name}"
