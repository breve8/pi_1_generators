import sys
from grid import Grid
from compute_generators import list_simple_gens
from draw import draw_cycle

with open(sys.argv[1]) as file:
    for line in file:
        grid = Grid(line)
        print("input grid:\n")
        print(grid.debug_print())
        # todo: draw connected components
        print("\nsmallest simple generators of fundamental group represented by vertex cycles:\n")
        cycles = list_simple_gens(grid)
        print('\n'.join(map(str, cycles)))
        print('\ndrawing the cycles:\n')
        for c in cycles: print(draw_cycle(list(c)))
        print('\n\n')
