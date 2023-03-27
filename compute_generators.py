# functions to detect cycles in the figure currently filling Grid (instantiated elsewhere); note this implementation mutates the grid, assuming for now that module will be invoked once per grid-instantiation

from grid import Grid

def extract_connected_components(grid: Grid):
    cpts = []
    while not grid.all_components_marked():
        cpts.append(split_component(grid))
        for (r, c) in cpts[-1]: grid.set(r, c, 'x') # marking corners on checked component so it won't be detected again
    return cpts

def find_start(grid):
    for r in range(grid.row_num):
        for c in range(grid.col_num):
            if grid.get(r, c) == '+': return (r,c)

def unexplored_edges(shape):
    for corner in shape:
        if any(shape[corner].values()): return True
    return False

def split_component(grid: Grid):  
    start = find_start(grid)
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

def next_vtx(cpt, curr, dir, max_row, max_col):
    r, c = curr
    if dir == 'r':
        return (r, min(x for x in range(c + 1, max_col + 1) if (r, x) in cpt))
    if dir == 'l':
        return (r, max(x for x in range(c - 1, -1, -1) if (r, x) in cpt))
    if dir == 'd':
        return (min(x for x in range(r + 1, max_row + 1) if (x, c) in cpt), c)
    if dir == 'u':
        return (max(x for x in range(r - 1, -1, -1) if (x, c) in cpt), c)

def cycle_start(component, grid, exclude):
    order = list(component) # lists in lexicographic order
    for corner in order:
        dirs = grid.directions(corner)
        if dirs['r'] and dirs['d'] and corner not in exclude: return corner
    return False

def generating_cycles(component, grid):
    rtn = set() # set of vertex cycles, convert to list of shapes (some of which might be the same shape, but not vtx set) later
    start_points = set()    # this construction forces any vertex in the grid to be the 'start' (top-left) point of at most one cycle, so we record them as they're found to stop the same cycle being recorded twice
    start = cycle_start(component, grid, start_points)
    while start:
        shape = [start]
        start_points.add(start) # todo: error check
        dir, shape_side = 'r', 'd'
        nxt = next_vtx(component, start, dir, grid.row_num, grid.col_num)
        while nxt != start:
            shape.append(nxt)
            dir, shape_side = navigate(grid, nxt, dir, shape_side)
            if not dir:
                shape = None
                break
            nxt = next_vtx(component, nxt, dir, grid.row_num, grid.col_num)
        if shape: rtn.add(tuple(shape))
        start = cycle_start(component, grid, start_points)
    return rtn

def navigate(grid, corner, incoming, shape_side):
    outgoing = grid.remove_incoming(grid.directions(corner), incoming)
    if outgoing[shape_side]: return shape_side, grid.opposite(incoming)
    if outgoing[incoming]: return incoming, shape_side
    if outgoing[grid.opposite(shape_side)]: return grid.opposite(shape_side), incoming
    print('could not navigate')
    return(None, None)

def list_simple_gens(grid):
    components = extract_connected_components(grid)
    rtn = []
    for cpt in components:
        rtn += generating_cycles(cpt, grid)
    return rtn


if __name__ == "__main__":
    pass