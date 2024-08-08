import itertools

def recurse(level, history):
    if level == 0:
        print(list(zip(*history)))
        input()
    else:
        for i in itertools.permutations([0, 1, 2, 3, 4], r=5):
            new_history = history.copy()
            new_history.append(i)
            recurse(level - 1, new_history)

recurse(7, [])
