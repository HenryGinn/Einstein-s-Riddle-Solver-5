from EinsteinRiddle import EinsteinRiddle

#my_puzzle = EinsteinRiddle("Einstein Riddle")
#my_puzzle = EinsteinRiddle("Henry Riddle")
my_puzzle = EinsteinRiddle("Rachel Riddle")
my_puzzle.set_problem_structure()
#my_puzzle.output_problem_structure()
#my_puzzle.set_clues()
#my_puzzle.output_clues()
#my_puzzle.display(size="half", colour="psycho")

my_puzzle.solution = [(0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1), (2, 2, 2, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3, 3), (4, 4, 4, 4, 4, 4, 4)]
my_puzzle.table()
