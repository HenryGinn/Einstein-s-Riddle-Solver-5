def capitalise(string):
    if type(string) is str:
        string = get_capitalised(string)
    return string

def get_capitalised(string):
    string_capitalised = [capitalise_word(word) for word in string.split(" ")]
    string_capitalised = " ".join(string_capitalised)
    return string_capitalised

def capitalise_word(word):
    first_letter = word[0]
    rest_of_word = word[1:]
    capitalised_word = first_letter.upper() + rest_of_word.lower()
    return capitalised_word


def get_list_string(non_indented):
    if isinstance(non_indented, str):
        return get_string_list_str(non_indented)
    else:
        return get_string_list_non_str(non_indented)

def get_string_list_str(non_indented):
    non_indented = non_indented.split("\n")
    if len(non_indented) > 1:
        return get_list_string(non_indented)
    else:
        return f"  {non_indented[0]}"

def get_string_list_non_str(non_indented):
    if hasattr(non_indented, "__iter__"):
        return get_indented_string(non_indented)
    else:
        return get_list_string(str(non_indented))

def get_indented_string(non_indented):
    output_string = "".join([f"{get_list_string(element)}\n"
                             for element in non_indented])
    return output_string
