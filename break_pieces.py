from sys import argv

class Grid():   # singleton wrapper class for state of grid
    grid = []
    row_num = 0
    col_num = 0

    @classmethod
    def from_string(cls, g):
        if g[0] == '\n': g = g[1:] # for some reason sample inputs start with newline?!
        rows = g.split('\n')
        cls.grid = list(map(list, rows))
        cls.row_num = len(cls.grid)
        cls.col_num = len(cls.grid[0])

    @classmethod
    def get(cls, row, column): return cls.grid[row][column]

    @classmethod
    def set(cls, row, column, val): cls.grid[row][column] = val

    @classmethod
    def clear(cls, point): cls.set(point[0], point[1], ' ')
    
    @classmethod
    def rows(cls): return cls.grid

    @classmethod
    def empty(cls):  # for purposes here, grid is empty when all corners removed
        return all(all(c != '+' for c in row) for row in cls.grid)
    


def break_pieces(g):
    Grid.from_string(g)
    pieces = []
    while not Grid.empty():
        print("hi")
        component = split_component()
        print(component)
        pieces += shapes(component)
    print(pieces)
    for cycle in pieces: print(draw(cycle))
    return list(map(draw, pieces))

def directions(corner):
    row, col = corner
    max_row = Grid.row_num - 1
    max_col = Grid.col_num - 1
    u = 1 if row > 0 and Grid.get(row-1, col) == '|' else 0
    d = 1 if row < max_row and Grid.get(row+1, col) == '|' else 0
    l = 1 if col > 0 and Grid.get(row, col-1) == '-' else 0
    r = 1 if col < max_col and Grid.get(row, col+1) == '-' else 0
    return {'u':u,'r':r,'d':d,'l':l}

def remove_incoming(dirs, dir):
    if dir == 'u': dirs['d'] = 0
    if dir == 'd': dirs['u'] = 0
    if dir == 'l': dirs['r'] = 0
    if dir == 'r': dirs['l'] = 0
    return dirs

def find_start():   # can prob replace w corners[0]?
    for r in range(Grid.row_num):
        for c in range(Grid.col_num):
            if Grid.get(r, c) == '+': return (r,c)

def unexplored_edges(shape):
    for corner in shape:
        if any(shape[corner].values()): return True
    return False

def split_component():  
    start = find_start()
    shape = {start:directions(start)}
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
    for corner in shape: Grid.clear(corner)
    return shape.keys()

def find_next(curr, dir):
    r,c = curr
    if dir == 'u':
        for i in range(r-1, -1, -1):
            if Grid.get(i,c) == '+':
                corner = (i,c)
                dirs = remove_incoming(directions(corner), dir)
                break
    if dir == 'd':
        for i in range(r+1, Grid.row_num):
            if Grid.get(i,c) == '+':
                corner = (i,c)
                dirs = remove_incoming(directions(corner), dir)
                break
    if dir == 'l':
        for i in range(c-1, -1, -1):
            if Grid.get(r,i) == '+':
                corner = (r,i)
                dirs = remove_incoming(directions(corner), dir)
                break
    if dir == 'r':
        for i in range(c+1, Grid.col_num):
            if Grid.get(r,i) == '+':
                corner = (r,i)
                dirs = remove_incoming(directions(corner), dir)
                break
    return corner, dirs

def find_top_left(component):
    order = list(component)
    for corner in order:
        dirs = directions(corner)
        if dirs['r'] and dirs['d']: return corner
    return False
    # return first coord in lex order (persist this?) that has a right outbound
    # edge (these will be stripped at start of shape traversal), False if none

def shapes(component):
    rtn = set() # set of vertex cycles, convert to list of shapes (some of which might be the same shape, but not vtx set) later
    start = find_top_left(component)
    while start:
        shape = [start]
        print(shape)
        dir, shape_side = 'r', 'd'
        nxt = next_vtx(component, start, dir)
        Grid.clear((start[0], start[1]+1))
        Grid.clear((nxt[0], nxt[1]-1))
        while nxt != start:
            # print(shape)
            shape.append(nxt)
            dir, shape_side = navigate(nxt, dir, shape_side)
            if not dir:
                shape = None
                break
            nxt = next_vtx(component, nxt, dir)
        if shape: rtn.add(tuple(shape))
        start = find_top_left(component)
    return rtn

def opposite(dir):
    if dir == 'r': return 'l'
    if dir == 'l': return 'r'
    if dir == 'u': return 'd'
    if dir == 'd': return 'u'
    if dir == 'hor': return 'vert'
    if dir == 'vert': return 'hor'
    print('invalid direction')

def navigate(corner, incoming, shape_side):
    outgoing = remove_incoming(directions(corner), incoming)
    if outgoing[shape_side]: return shape_side, opposite(incoming)
    if outgoing[incoming]: return incoming, shape_side
    if outgoing[opposite(shape_side)]: return opposite(shape_side), incoming
    print('could not navigate')
    return(None, None)

def next_vtx(cpt, curr, dir):
    r,c = curr
    inc = 1 if dir in ('r', 'd') else -1
    i = 1
    if dir in ('l', 'r'):
        while True:
            if (r, c + (inc*i)) in cpt: return (r, c + (inc*i))
            i += 1
    while True:
        if (r + (inc*i), c) in cpt: return (r + (inc*i), c)
        i += 1

def edge_char(ornt): return '-' if ornt == 'hor' else '|'

def side_length(curr, nxt, ornt):
    if ornt == 'hor': return nxt[1] - curr[1]
    return nxt[0] - curr[0]

def collinear(prev, curr, nxt):
    return any((prev[i] == curr[i] and curr[i] == nxt[i]) for i in (0, 1))

def add_side(shape, pos, ornt, l, start):
    # print(pos)
    shape[pos[0]][pos[1]] = start
    axis = 0 if ornt == 'vert' else 1   # just use this everywhere instead of ornt? or better, ornt enum (as well as dirs) with axis property
    nxt_pos = pos.copy()
    nxt_pos[axis] += l
    # print(nxt_pos)
    if nxt_pos[axis] < 0:  # can only happen if need to expand left
        mod = abs(nxt_pos[axis])
        for i,_ in enumerate(shape): shape[i] = ([' '] * mod) + shape[i]
        nxt_pos[axis] += mod
        pos[axis] += mod
    elif axis == 0 and nxt_pos[0] > len(shape):
        for _ in range(nxt_pos[0] - (len(shape) - 1)):
            shape.append([' '] * len(shape[0]))  # all rows same length?
    elif axis == 1 and nxt_pos[1] > len(shape[0]):
        for row in shape: row += ([' '] * (nxt_pos[1] - len(shape[0]) + 1))
    step = -1 if l < 0 else 1
    for i in range(1, abs(l)):
        # print(shape)
        # print(i*(1 - axis)*(step))
        # print(i*(axis)*(step))
        shape[pos[0] + (i*(1 - axis)*(step))][pos[1] + (i*(axis)*(step))] = edge_char(ornt)
    return shape, nxt_pos

def draw(cycle):
    shape = [['+']]
    ornt = 'hor'
    coord_map = {'hor':0, 'vert':1}
    pos = [0,0]
    for i, vtx in enumerate(cycle):
        nxt = cycle[(i + 1)%len(cycle)]
        if nxt[coord_map[ornt]] != vtx[coord_map[ornt]]: ornt = opposite(ornt)
        # print(ornt, shape)
        l = side_length(vtx, nxt, ornt)  # can be -ve
        # print(vtx, nxt, l)
        if i >= 1 and collinear(cycle[i-1], vtx, nxt):
            start = edge_char(ornt)
        else: start = '+'
        # print(start)
        shape, pos = add_side(shape, pos, ornt, l, start)
    return '\n'.join(''.join(row) for row in shape)


# uncomment next line if you prefer raw error messages
# raw_errors = True
break_pieces('\n         +------------+--+      +--+\n         |            |  |      |  |\n         | +-------+  |  |      |  |\n         | |       |  |  +------+  |\n         | |       |  |            |\n         | |       |  |    +-------+\n         | +-------+  |    |        \n +-------+            |    |        \n |       |            |    +-------+\n |       |            |            |\n +-------+            |            |\n         |            |            |\n    +----+---+--+-----+------------+\n    |    |   |  |     |            |\n    |    |   |  +-----+------------+\n    |    |   |                     |\n    +----+---+---------------------+\n    |    |                         |\n    |    | +----+                  |\n+---+    | |    |     +------------+\n|        | |    |     |             \n+--------+-+    +-----+             ')

# test 2