from UserFacing.ProblemStructure.Characteristic import Characteristic
from UserFacing.ProblemStructure.Relations import Relations
from UserFacing.ProblemStructure.RelationName import RelationName
from Utils import get_int_input

class FamilyCharacteristic(Characteristic):

    def __init__(self, ID, problem):
        Characteristic.__init__(self, ID, problem)
        self.type = "Family"
        self.relations = []
        self.relation_names = []

    def set_characteristic_name(self):
        self.name = "Family"

    def set_property_names(self):
        self.set_family_tree_information()
        self.set_relations()
        self.create_relation_names()

    def set_family_tree_information(self):
        self.set_in_laws()
        self.set_generations()
        self.set_spouses()
        self.set_same_sex()

    def set_in_laws(self):
        prompt = ("\nAre there any in-law relations?\n"
                  "1: No\n"
                  "2: Maybe\n")
        in_laws_user_input = get_int_input(prompt, 1, 2)
        self.in_laws = {1: False, 2: True}[in_laws_user_input]

    def set_generations(self):
        self.set_generations_young()
        self.set_generations_old()

    def set_generations_young(self):
        prompt = ("\nHow many generations are below some element?\n"
                  "If you do not know, enter -1\n")
        self.generations_young = get_int_input(prompt, -1, self.problem.element_count - 1)
        self.process_generations_young()

    def process_generations_young(self):
        if self.generations_young == -1:
            self.generations_young = self.problem.element_count - 1
    
    def set_generations_old(self):
        prompt = ("\nHow many generations are above that same element?\n"
                  "If you do not know, enter -1\n")
        self.generations_old = get_int_input(prompt, -1, self.problem.element_count - 1)
        self.process_generations_old()
        print(self.generations_old)

    def process_generations_old(self):
        if self.generations_old == -1:
            self.generations_old = self.problem.element_count - 1

    def set_spouses(self):
        prompt = ("\nAre any spouses present in the family?\n"
                  "1: No\n"
                  "2: Maybe\n")
        spouses_user_input = get_int_input(prompt, 1, 2)
        self.spouses = {1: False, 2: True}[spouses_user_input]

    def set_same_sex(self):
        prompt = ("\nAre any same-sex relations present in the family?\n"
                  "1: No\n"
                  "2: Maybe\n")
        same_sex_user_input = get_int_input(prompt, 1, 2)
        self.same_sex = {1: False, 2: True}[same_sex_user_input]

    def set_relations(self):
        relations = Relations(self)
        relations.set_relations()
        self.relations = relations.relations
        
    def create_relation_names(self):
        relation_objects = [RelationName(relation) for relation in self.relations]
        self.property_names = [relation_obj.name for relation_obj in relation_objects]

    def get_data_dict(self):
        data_dict = self.get_base_data_dict()
        self.set_data_dict_properties(data_dict)
        return data_dict

    def set_data_dict_properties(self, data_dict):
        relations_iterable = zip(self.relations, self.property_names)
        properties = [self.get_relation_dict(relation, relation_name)
                      for relation, relation_name in relations_iterable]
        data_dict["Properties"] = properties
        return data_dict

    def get_relation_dict(self, relation, relation_name):
        relation_dict = {"Relation List": relation,
                         "Relation Name": relation_name}
        return relation_dict

    def load_from_dict(self, characteristic_dict):
        self.name = characteristic_dict["Name"]
        relation_data = [list(relation.values()) for relation in characteristic_dict["Properties"]]
        self.relations, self.property_names = zip(*relation_data)
        
