# functions to detect cycles in the figure currently filling Grid (instantiated elsewhere); note this implementation mutates the grid, assuming for now that module will be invoked once per grid-instantiation

import grid

def extract_connected_components():
    cpts = []
    while not grid.has_unmarked_components():
        cpts.append(split_component())
        for (r, c) in cpts[-1]: grid.set(r, c, 'x') # marking corners on checked component so it won't be detected again
    return cpts

def find_start():
    for r in range(Grid.row_num):
        for c in range(Grid.col_num):
            if grid.get(r, c) == '+': return (r,c)

def unexplored_edges(shape):
    for corner in shape:
        if any(shape[corner].values()): return True
    return False

def split_component():  
    start = find_start()
    component = {start: grid.directions(start)}
    while unexplored_edges(component):    # build up list of corners & valencies until all connections explored
        next_lvl = dict()
        for corner in component:
            for dir in ('u', 'r', 'd', 'l'):
                if component[corner][dir] == 0: continue
                next_corner, dirs = grid.find_next_corner(corner, dir)
                if next_corner in next_lvl:
                    next_lvl[next_corner] = grid.remove_incoming(next_lvl[next_corner], dir)
                else: next_lvl[next_corner] = dirs
                component[corner][dir] = 0
        component.update(next_lvl)
    return component.keys()