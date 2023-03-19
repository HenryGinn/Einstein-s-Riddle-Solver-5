import numpy as np
import math

def get_int_input(prompt, lower_bound=None, upper_bound=None):
    lower_bound, upper_bound = get_bounds(lower_bound, upper_bound)
    int_input = get_int_input_with_bounds(prompt, lower_bound, upper_bound)
    return int_input

def get_bounds(lower_bound, upper_bound):
    lower_bound = get_bound(lower_bound, -np.inf)
    upper_bound = get_bound(upper_bound, np.inf)
    check_valid_bounds(lower_bound, upper_bound)
    return lower_bound, upper_bound

def get_bound(bound, default):
    if bound is None:
        bound = default
    return bound

def check_valid_bounds(lower_bound, upper_bound):
    if lower_bound != -np.inf and upper_bound != np.inf:
        if math.floor(upper_bound) - math.ceil(lower_bound) < 0:
            raise Exception(("Bounds do not contain an integer\n"
                             f"Lower bound: {lower_bound}\n"
                             f"Upper bound: {upper_bound}"))

def get_int_input_with_bounds(prompt, lower_bound, upper_bound):
    input_valid = False
    while input_valid is False:
        int_input, input_valid = attempt_get_int_input(prompt, lower_bound, upper_bound)
    return int_input

def attempt_get_int_input(prompt, lower_bound, upper_bound):
    int_input = input(f"{prompt}")
    check_functions, args = get_int_check_functions(lower_bound, upper_bound)
    int_input, input_valid = check_int_valid(int_input, check_functions, args)
    return int_input, input_valid

def get_int_check_functions(lower_bound, upper_bound):
    check_functions = [check_is_integer, check_lower_bound, check_upper_bound]
    args = ([], [lower_bound], [upper_bound])
    return check_functions, args

def check_int_valid(int_input, check_functions, args):
    for check_function, args in zip(check_functions, args):
         if check_function(int_input, *args) is False:
             return None, False
    return int(int_input), True

def check_is_integer(int_input):
    try:
        int(int_input)
        return True
    except:
        return bad_input_response("Sorry, you must enter an integer")

def check_lower_bound(int_input, lower_bound):
    if lower_bound <= int(int_input):
        return True
    else:
        return bad_input_response(f"Sorry, your input must be at least {lower_bound}")

def check_upper_bound(int_input, upper_bound):
    if int(int_input) <= upper_bound:
        return True
    else:
        return bad_input_response(f"Sorry, your input must be at most {upper_bound}")

def bad_input_response(prompt):
    print(prompt)
    return False

def get_yes_no_input(prompt):
    new_prompt = (f"{prompt}\n"
                  "1: Yes\n"
                  "2: No\n")
    yes_no_input = get_int_input(new_prompt, lower_bound=1, upper_bound=2)
    return yes_no_input


def get_non_repeating_input(prompt, input_list, get_input_function=None):
    get_input_function = get_get_input_function(get_input_function)
    input_is_valid = False
    while input_is_valid is False:
        user_input, input_is_valid = attempt_get_non_repeating_input(prompt, input_list, get_input_function)
    return user_input

def get_get_input_function(get_input_function):
    if get_input_function is None:
        get_input_function = input
    return get_input_function

def attempt_get_non_repeating_input(prompt, input_list, get_input_function):
    user_input = get_input_function(prompt)
    user_input = capitalise(user_input)
    user_input, input_is_valid = process_user_input(user_input, input_list)
    return user_input, input_is_valid

def process_user_input(user_input, input_list):
    if str(user_input) in [str(item) for item in input_list]:
        return bad_user_input(input_list)
    else:
        return user_input, True

def bad_user_input(input_list):
    print(("Sorry, that has already been used\n"
           "Here are the previously given inputs:"))
    for user_input in input_list:
        print(user_input)
    return None, False


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


def get_consecutive_list(input_list, length):
    consecutive_list = [input_list[index:index + length]
                        for index in range(len(input_list) + 1 - length)]
    return consecutive_list


def get_list_string(non_indented, indent=0):
    if isinstance(non_indented, list) or isinstance(non_indented, tuple):
        return get_indented_list(non_indented, indent)
    elif isinstance(non_indented, str):
        return get_indented_string(non_indented, indent)
    else:
        raise Exception(f"Cannot convert object of type {type(non_indented)} to list string")

def get_indented_list(non_indented, indent):
    joining_string = "\n" + f"{indent * ' '}"
    output_string = "".join([f"{joining_string}{element}" for element in non_indented])
    return output_string

def get_indented_string(non_indented, indent):
    joining_string = "\n" + f"{indent * ' '}"
    output_string = "".join([f"{joining_string}{element}" for element in non_indented.split("\n")])
    return output_string
