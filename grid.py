def opposite(dir):
    if dir == 'r': return 'l'
    if dir == 'l': return 'r'
    if dir == 'u': return 'd'
    if dir == 'd': return 'u'
    if dir == 'hor': return 'vert'
    if dir == 'vert': return 'hor'
    print(f'invalid direction: {dir}')

def remove_incoming(dirs, dir):
    dirs[opposite(dir)] = 0
    return dirs

class Grid():
    def __init__(self, txt_input):
        if txt_input[0] == '\n': txt_input = txt_input[1:] # codewars sample inputs start with newline?
        rows = txt_input.split('\\n')
        self.row_num = len(rows)
        self.col_num = max(len(row) for row in rows)
        self.grid = list(map(list, rows))
        for row in self.grid:
            row += [' '] * (self.col_num - len(row))

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)
    
    @staticmethod
    def pad_str(n: int, leading=2):
        return str(n).zfill(leading)

    def debug_print(self):
        out = ['  ' + ''.join(map(self.pad_str, range(self.col_num)))]
        for r in range(self.row_num):
            out += [self.pad_str(r) + ' '.join(char for char in self.grid[r]) + '  ' + self.pad_str(r)]
        out += ['  ' + ''.join(map(self.pad_str, range(self.col_num)))]
        return '\n'.join(out)

    def get(self, row, column):
        return self.grid[row][column]

    def is_corner(self, row, column):
        return self.get(row, column) in ('+', 'x')

    def mark_corner(self, row, column):
        if not self.is_corner(row, column): raise ValueError(f"tried to mark ({row},{column}), not a corner")
        self.grid[row][column] = 'x'

    def first_unmarked(self):
        for r in range(self.row_num):
            for c in range(self.col_num):
                if self.get(r, c) == '+': return (r,c)
        
    def clear(self, point): self.set(point[0], point[1], ' ')

    def rows(self): return self.grid

    def all_components_marked(self):
        return all(all(c != '+' for c in row) for row in self.grid)

    def directions(self, corner):    # data returned represents outgoing edges at a vertex
        row, col = corner
        max_row = self.row_num - 1
        max_col = self.col_num - 1
        u = 1 if row > 0 and self.get(row-1, col) in ('|', '+', 'x') else 0
        d = 1 if row < max_row and self.get(row+1, col) in ('|', '+', 'x') else 0
        l = 1 if col > 0 and self.get(row, col-1) in ('-', '+', 'x') else 0
        r = 1 if col < max_col and self.get(row, col+1) in ('-', '+', 'x') else 0
        return {'u':u, 'r':r, 'd':d, 'l':l}

    def find_next_corner(self, curr, dir):
        r, c = curr
        axis_to_step = 1 if dir in ('u', 'd') else 0
        inc = -1 if dir in ('u', 'l') else 1
        i = inc
        while True:
            r_inc = r + axis_to_step*i
            c_inc = c + (1 - axis_to_step)*i
            if r_inc < 0 or c_inc < 0 or r_inc >= self.row_num or c_inc >= self.col_num:
                raise ValueError(f"could not find next corner from {curr} in direction {dir}")
                break
            if self.is_corner(r_inc, c_inc):
                corner = (r_inc, c_inc)
                dirs = remove_incoming(self.directions(corner), dir)
                return corner, dirs
            # todo: change return type?
            i += inc