from Utils.IntInput import get_int_input
from Utils.Strings import capitalise

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

def get_options_input(base_prompt, options):
    if len(options) == 1:
        return 1
    else:
        return get_subtype_input_from_user(base_prompt, options)

def get_subtype_input_from_user(base_prompt, options):
    prompt = get_options_prompt(base_prompt, options)
    options_count = len(options)
    options_input = get_int_input(prompt, lower_bound=1,
                                  upper_bound=options_count)
    return options_input

def get_options_prompt(base_prompt, options):
    prompt = f"{base_prompt}\n"
    for index, option in enumerate(options):
        prompt += f"{index + 1}: {option}\n"
    return prompt
