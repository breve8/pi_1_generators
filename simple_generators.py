import sys
from grid import Grid
from compute_generators import list_simple_gens

with open(sys.argv[1]) as file:
    for line in file:
        grid = Grid(line)
        print("input grid:\n")
        print(grid)
        # todo: draw connected components
        print("\nsmallest simple generators of fundamental group represented by vertex cycles:\n")
        print(list_simple_gens(grid))
        # print('\n\n\n')