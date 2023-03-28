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

def cycle_start(order, grid, exclude):
    for corner in order:
        dirs = grid.directions(corner)
        if dirs['r'] and dirs['d'] and corner not in exclude: return corner
    return False

def generating_cycles(component, grid):
    rtn = set() # set of vertex cycles, convert to list of shapes (some of which might be the same shape, but not vtx set) later
    non_start_points = set()    # stores coordinates of corners that should be excluded as start points of potential cycles, either because they have already been used or lie on a "free face" of the boundary
    component = sorted(list(component)) # lists in lexicographic order
    start_point = cycle_start(component, grid, non_start_points)
    bdry = boundary(component, grid)
    while start_point:
        shape = [start_point]
        non_start_points.add(start_point)
        dir, shape_side = 'r', 'd'
        nxt = next_vtx(component, start_point, dir, grid.row_num, grid.col_num)
        while nxt != start_point:
            if nxt in non_start_points and shape_side == 'r':   # cycle already counted
                shape = None
                break
            if nxt in bdry and dir == 'l' and \
                set(bdry[nxt]) == {'d', 'r'}:    # indented free face in the boundary
                non_start_points.add(nxt)
            shape.append(nxt)
            dir, shape_side = navigate(grid, nxt, dir, shape_side)
            if not dir:
                shape = None
                break
            nxt = next_vtx(component, nxt, dir, grid.row_num, grid.col_num)
        if shape: rtn.add(tuple(shape))
        start_point = cycle_start(component, grid, non_start_points)
    return rtn

def navigate(grid, corner, incoming, shape_side):
    outgoing = grid.remove_incoming(grid.directions(corner), incoming)
    if outgoing[shape_side]: return shape_side, grid.opposite(incoming)
    if outgoing[incoming]: return incoming, shape_side
    if outgoing[grid.opposite(shape_side)]: return grid.opposite(shape_side), incoming
    print('could not navigate')
    return(None, None)

def navigate_boundary(grid, corner, incoming, int_side):
    outgoing = grid.remove_incoming(grid.directions(corner), incoming)
    if outgoing[grid.opposite(int_side)]: return grid.opposite(int_side), incoming
    if outgoing[incoming]: return incoming, int_side
    if outgoing[int_side]: return int_side, grid.opposite(incoming)

def boundary(component, grid):
    # assume component is list of vertices in lex order, return set of vertices in component boundary, together with the pair of incident edges at each that form a boundary segment
    start = component[0]
    bdry = {start:['d', 'r']}
    dir, int_side = 'r', 'd'
    nxt = next_vtx(component, start, dir, grid.row_num, grid.col_num)
    while nxt != start:
        bdry[nxt] = [grid.opposite(dir)]
        dir, int_side = navigate_boundary(grid, nxt, dir, int_side)
        bdry[nxt].append(dir)
        nxt = next_vtx(component, nxt, dir, grid.row_num, grid.col_num)
    return bdry

def list_simple_gens(grid):
    components = extract_connected_components(grid)
    rtn = []
    for cpt in components:
        rtn += generating_cycles(cpt, grid)
    return rtn