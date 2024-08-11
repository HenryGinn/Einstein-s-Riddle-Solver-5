from cvxopt.glpk import ilp
import numpy as np
from cvxopt import matrix


def get_blank():
    return np.zeros([elements] * factors)

def get_slice():
    return [slice(0, elements) for k in range(factors)]

def get_index(name):
    return np.array(np.nonzero(names == name)).reshape(-1)

def get_match(name_1, name_2):
    index_1 = get_index(name_1)
    index_2 = get_index(name_2)
    a = get_blank()
    s = get_slice()
    s[index_1[0]] = index_1[1]
    a[*s] = 1
    s[index_2[0]] = index_2[1]
    a[*s] = 0
    s = get_slice()
    s[index_2[0]] = index_2[1]
    a[*s] = 1
    s[index_1[0]] = index_1[1]
    a[*s] = 0
    return (np.array([a]), np.array([0]))

def get_unmatch(name_1, name_2):
    index_1 = get_index(name_1)
    index_2 = get_index(name_2)
    a = get_blank()
    s = get_slice()
    s[index_1[0]] = index_1[1]
    s[index_2[0]] = index_2[1]
    a[*s] = 1
    return (np.array([a]), np.array([0]))

def get_exactly_left(name_1, name_2):
    # name_1 is exactly left of name_2
    index_1 = get_index(name_1)
    index_2 = get_index(name_2)
    a = np.zeros([elements] + [elements] * factors)
    for i in range(elements):
        s = get_slice()
        s[index_1[0]] = index_1[1]
        s[-1] = i
        a[i, *s] = 1
        s = get_slice()
        s[index_2[0]] = index_2[1]
        s[-1] = [j for j in range(elements) if j-1 != i]
        a[i, *s] += 1
    return (a, np.ones(elements))

def get_exactly_right(name_1, name_2):
    # name_1 is exactly right of name_2
    index_1 = get_index(name_1)
    index_2 = get_index(name_2)
    a = np.zeros([elements] + [elements] * factors)
    for i in range(elements):
        s = get_slice()
        s[index_1[0]] = index_1[1]
        s[-1] = i
        a[i, *s] = 1
        s = get_slice()
        s[index_2[0]] = index_2[1]
        s[-1] = [j for j in range(elements) if j+1 != i]
        a[i, *s] += 1
    return (a, np.ones(elements))

def get_right(name_1, name_2):
    # name_1 is right of name_2
    index_1 = get_index(name_1)
    index_2 = get_index(name_2)
    a = np.zeros([elements] + [elements] * factors)
    for i in range(elements):
        s = get_slice()
        s[index_1[0]] = index_1[1]
        s[-1] = i
        a[i, *s] = 1
        s = get_slice()
        s[index_2[0]] = index_2[1]
        s[-1] = slice(i, elements)
        a[i, *s] += 1
    return (a, np.ones(elements))

def get_left(name_1, name_2):
    # name_1 is left of name_2
    index_1 = get_index(name_1)
    index_2 = get_index(name_2)
    a = np.zeros([elements] + [elements] * factors)
    for i in range(elements):
        s = get_slice()
        s[index_1[0]] = index_1[1]
        s[-1] = i
        a[i, *s] = 1
        s = get_slice()
        s[index_2[0]] = index_2[1]
        s[-1] = slice(0, i+1)
        a[i, *s] += 1
    return (a, np.ones(elements))

def get_next_to(name_1, name_2):
    index_1 = get_index(name_1)
    index_2 = get_index(name_2)
    a = np.zeros([elements] + [elements] * factors)
    for i in range(elements):
        s = get_slice()
        s[index_1[0]] = index_1[1]
        s[-1] = i
        a[i, *s] = 1
        s = get_slice()
        s[index_2[0]] = index_2[1]
        s[-1] = [j for j in range(elements) if (j-1 != i and j+1 != i)]
        a[i, *s] += 1
    return (a, np.ones(elements))

puzzle = "Test"
puzzle = "Rachel"
#puzzle = "Einstein"

match puzzle:
    case "Test":
        names = np.array([
            ["Amy", "Boris", "Charlie", "Devin"],
            ["A", "B", "C", "D"],
            ["1", "2", "3", "4"]])
    case "Rachel":
        names = np.array([
            ["Raffalo", "Moxx", "Boe", "Lady", "Jabe"],
            ["Argolis", "Vortis", "Marinus", "Rax", "Terra"],
            ["Jazz", "Reggae", "Metal", "EDM", "Punk"],
            ["Beans", "Worms", "Pudding", "Caviar", "Pizza"],
            ["Switch", "Spiders", "Baby", "Ring Pop", "Nothing"],
            ["TV", "Pranking", "Chess", "Yoga", "Surfing"],
            ["1", "2", "3", "4", "5"]])
    case "Einstein":
        names = np.array([
            ["Brit", "Swede", "Dane", "German", "Nor"],
            ["Red", "Green", "White", "Yellow", "Blue"],
            ["Dog", "Bird", "Cat", "Horse", "Fish"],
            ["Tea", "Coffee", "Milk", "Beer", "Water"],
            ["Pall Mall", "Dunhill", "Blend", "Bluemaster", "Prince"],
            ["1", "2", "3", "4", "5"]])

factors, elements = names.shape

match puzzle:
    case "Test":
        constraints = [get_next_to("A", "Charlie")]
    case "Rachel":
        constraints = [
            get_next_to("Raffalo", "Argolis"),
            get_exactly_right("Switch", "Beans"),
            get_match("TV", "Jazz"),
            get_match("Moxx", "Pranking"),
            get_next_to("Reggae", "Spiders"),
            get_exactly_right("Moxx", "Worms"),
            get_right("Beans", "Chess"),
            get_right("Raffalo", "Beans"),
            get_next_to("Boe", "Metal"),
            get_unmatch("2", "Lady"),
            get_unmatch("3", "Lady"),
            get_unmatch("4", "Lady"),
            get_match("Rax", "Chess"),
            get_exactly_left("EDM", "Yoga"),
            get_exactly_left("Jabe", "Raffalo"),
            get_next_to("Baby", "Surfing"),
            get_next_to("TV", "Reggae"),
            get_exactly_right("Ring Pop", "Punk"),
            get_next_to("Vortis", "Ring Pop"),
            get_match("Vortis", "Surfing"),
            get_exactly_left("Pudding", "Jazz"),
            get_right("Caviar", "Vortis"),
            get_match("2", "Terra"),
            get_exactly_left("Nothing", "Yoga")]
    case "Einstein":
        constraints = [
            get_match("Brit", "Red"),
            get_match("Swede", "Dog"),
            get_match("Dane", "Tea"),
            get_right("White", "Green"),
            get_match("Green", "Coffee"),
            get_match("Pall Mall", "Bird"),
            get_match("Yellow", "Dunhill"),
            get_match("3", "Milk"),
            get_match("Nor", "1"),
            get_next_to("Blend", "Cat"),
            get_next_to("Horse", "Dunhill"),
            get_match("Bluemaster", "Beer"),
            get_match("German", "Prince"),
            get_match("Nor", "Blue"),
            get_next_to("Blend", "Water")
            ]

def find(name_1, name_2):
    return (find_name(name_1), find_name(name_2))

def find_name(name):
    for i in solution:
        if name in i:
            return int(i[-1])

def check_solution():
    clues_check = np.array([
        find("Raffalo", "Argolis") in next_to,
        find("Switch", "Beans") in exactly_right_of,
        find("Reggae", "Spiders") in next_to,
        find("Moxx", "Worms") in exactly_right_of,
        find("Beans", "Chess") in right_of,
        find("Raffalo", "Beans") in right_of,
        find("Boe", "Metal") in next_to,
        find_name("Lady") in [1, 5],
        find("Rax", "Chess") in matches,
        find("EDM", "Yoga") in exactly_left_of,
        find("Jabe", "Raffalo") in exactly_left_of,
        find("Baby", "Surfing") in next_to,
        find("TV", "Reggae") in next_to,
        find("Ring Pop", "Punk") in exactly_right_of,
        find("Vortis", "Ring Pop") in next_to,
        find("Vortis", "Surfing") in matches,
        find("Pudding", "Jazz") in exactly_left_of,
        find("Caviar", "Vortis") in right_of,
        find_name("Terra") == 2,
        find("Nothing", "Yoga") in exactly_left_of])
    if np.all(clues_check):
        print("\n\n\n\nFOUND SOLUTION\n\n\n\n")

next_to = [(1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3), (4, 5), (5, 4)]
exactly_right_of = [(2, 1), (3, 2), (4, 3), (5, 4)]
exactly_left_of = [(1, 2), (2, 3), (3, 4), (4, 5)]
right_of = [(2, 1), (3, 2), (4, 3), (5, 4), (3, 1), (4, 1), (5, 1), (4, 2), (5, 2), (5, 3)]
left_of = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (3, 5)]
matches = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
unmatches = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2),
             (3, 4), (3, 5), (4, 1), (4, 2), (4, 3), (4, 5), (5, 1), (5, 2), (5, 3), (5, 4)]

# Rook problem constraints
rooks = np.zeros([elements*factors] + [elements] * factors)
for i in range(factors):
    for j in range(elements):
        s = get_slice()
        s[i] = j
        rooks[i * elements + j, *s] = 1

not_unique = True
while not_unique:
    constraints_A, constraints_b = list(zip(*constraints))
    constraints_A = np.concatenate(constraints_A, axis=0)
    constraints_b = np.concatenate(constraints_b, axis=0)
    A = np.concatenate((rooks, constraints_A), axis=0)
    D = constraints_A
    A = A.reshape(-1, elements**factors)
    b = np.concatenate((np.ones(elements*factors), constraints_b))
    c = -np.ones(A.shape[1])

    (status, values) = ilp(matrix(c), matrix(A), matrix(b), B=set(range(elements**factors)))
    values = np.array(values).reshape([elements] * factors)

    indexes = np.array(np.where(values > 0.1)).transpose()
    indexes = sorted(indexes, key=lambda x: x[-1])
    solution = [[names[j][i[j]] for j in range(factors)] for i in indexes]
    if puzzle == "Rachel":
        check_solution()
    else:
        not_unique = False

    if len(indexes) < elements:
        not_unique = False
    else:
        for i in solution:
            print(", ".join(i))
        constraints.append((np.array([values]), np.array([elements-1])))
        print("")
