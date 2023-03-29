from grid import opposite

def side_length(curr, nxt, ornt):
    if ornt == 'hor': return nxt[1] - curr[1]
    return nxt[0] - curr[0]

def edge_char(ornt): return '-' if ornt == 'hor' else '|'

def collinear(prev, curr, nxt):
    return any((prev[i] == curr[i] and curr[i] == nxt[i]) for i in (0, 1))

def draw_cycle(cycle):
    shape = [['+']]
    ornt = 'hor'
    coord_map = {'hor':0, 'vert':1}
    pos = [0,0]
    for i, vtx in enumerate(cycle):
        nxt = cycle[(i + 1)%len(cycle)]
        if nxt[coord_map[ornt]] != vtx[coord_map[ornt]]: ornt = opposite(ornt)
        l = side_length(vtx, nxt, ornt)  # can be -ve
        start = edge_char(ornt) if (i >= 1 and collinear(cycle[i-1], vtx, nxt)) else '+'
        shape, pos = add_side(shape, pos, ornt, l, start)
    return '\n'.join(''.join(row) for row in shape)

def add_side(shape, pos, ornt, length, start):
    shape[pos[0]][pos[1]] = start
    axis_of_travel = 0 if ornt == 'vert' else 1   # just use this everywhere instead of ornt? or better, ornt enum (as well as dirs) with axis property (todo)
    nxt_pos = pos.copy()
    nxt_pos[axis_of_travel] += length
    if nxt_pos[axis_of_travel] < 0:  # only happens when we need to expand left, todo: extend to support upwards expansion
        mod = abs(nxt_pos[axis_of_travel])
        for i,_ in enumerate(shape): shape[i] = ([' '] * mod) + shape[i]
        for vtx in (pos, nxt_pos): vtx[axis_of_travel] += mod
    elif axis_of_travel == 0 and nxt_pos[0] > (len(shape) - 1):
        for _ in range(nxt_pos[0] - (len(shape) - 1)):
            shape.append([' '] * len(shape[0]))
    elif axis_of_travel == 1 and nxt_pos[1] > (len(shape[0]) - 1):
        offset = nxt_pos[1] - len(shape[0]) + 1
        for row in shape: row += ([' ']*offset)
    step = -1 if length < 0 else 1
    for i in range(1, abs(length)):
        shape[pos[0] + (i*(1 - axis_of_travel)*step)][pos[1] + (i*axis_of_travel*step)] = edge_char(ornt)
    return shape, nxt_pos