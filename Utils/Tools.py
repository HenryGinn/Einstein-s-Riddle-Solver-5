def get_consecutive_list(input_list, length):
    consecutive_list = [input_list[index:index + length]
                        for index in range(len(input_list) + 1 - length)]
    return consecutive_list
