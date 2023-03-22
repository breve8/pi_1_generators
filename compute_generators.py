# functions to detect cycles in the figure currently filling Grid (instantiated elsewhere); note this implementation mutates the grid, assuming for now that module will be invoked once per grid-instantiation

from grid import Grid

def extract_connected_components():
    cpts = []
    while not Grid.has_unmarked_components():
        cpts.append(split_component())
        for (r, c) in cpts[-1]: Grid.set(r, c, 'x') # marking corners on checked component so it won't be detected again
    return cpts

def find_start():
    for r in range(Grid.row_num):
        for c in range(Grid.col_num):
            if Grid.get(r, c) == '+': return (r,c)

def split_component():  
    # find top-left corner in first unmarked component
    start = find_start()
    shape = {start: directions(start)}
    while unexplored_edges(shape):    # build shape as list of
                                      # corners & valencies
        next_lvl = dict()
        for corner in shape:
            for dir in ('u', 'r', 'd', 'l'):
                if shape[corner][dir] == 0: continue
                nxt_corner, dirs = find_next(corner, dir)
                if nxt_corner in next_lvl:
                    next_lvl[nxt_corner] = remove_incoming(next_lvl[nxt_corner], dir)
                else: next_lvl[nxt_corner] = dirs
                shape[corner][dir] = 0
        shape.update(next_lvl)
    return shape.keys()