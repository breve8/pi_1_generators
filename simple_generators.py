import sys
from grid import Grid
import compute_generators

with open(sys.argv[1]) as file:
    for line in file:
        grid = Grid(line)
        print("input grid:\n")
        print(grid.debug_print())
        # todo: draw connected components
        print("\nsmallest simple generators of fundamental group represented by vertex cycles:\n")
        cycles = compute_generators.list_simple_gens(grid)
        print(cycles)
        # print('\n\n\n')