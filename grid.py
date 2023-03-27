class Grid():
    def __init__(self, txt_input):
        if txt_input[0] == '\n': txt_input = txt_input[1:] # codewars sample inputs start with newline?
        rows = txt_input.split('\\n')
        self.grid = list(map(list, rows))
        self.row_num = len(self.grid)
        self.col_num = len(self.grid[0])

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def get(self, row, column):
        return self.grid[row][column]

    def is_corner(self, row, column):
        return self.get(row, column) in ('+', 'x')

    def set(self, row, column, val): self.grid[row][column] = val

    def clear(self, point): self.set(point[0], point[1], ' ')

    def rows(self): return self.grid


    def has_unmarked_components(self):
        return all(all(c != '+' for c in row) for row in self.grid)


    def directions(self, corner):    # data returned represents outgoing edges at a vertex
        row, col = corner
        max_row = row_num - 1
        max_col = col_num - 1
        u = 1 if row > 0 and self.get(row-1, col) == '|' else 0
        d = 1 if row < max_row and self.get(row+1, col) == '|' else 0
        l = 1 if col > 0 and self.get(row, col-1) == '-' else 0
        r = 1 if col < max_col and self.get(row, col+1) == '-' else 0
        return {'u':u,'r':r,'d':d,'l':l}

    @staticmethod
    def opposite(dir):
        if dir == 'r': return 'l'
        if dir == 'l': return 'r'
        if dir == 'u': return 'd'
        if dir == 'd': return 'u'
        if dir == 'hor': return 'vert'
        if dir == 'vert': return 'hor'
        printf('invalid direction: {dir}')


    @staticmethod
    def remove_incoming(dirs, dir):
        dirs[Grid.opposite(dir)] = 0
        return dirs

    def find_next_corner(self, curr, dir):
        r, c = curr
        axis_to_step = 1 if dir in ('u', 'd') else 0
        inc = -1 if dir in ('u', 'l') else 1
        i = inc
        while True:
            r_inc = r + axis_to_step*i
            c_inc = c + (1 - axis_to_step)*i
            if r_inc < 0 or c_inc < 0 or r_inc >= self.row_num or c_inc >= self.col_num:
                printf("could not find next corner from {curr} in direction {dir}")
                break
            if is_corner(r_inc, c_inc):
                corner = (r_inc, c_inc)
                dirs = Grid.remove_incoming(self.directions(corner), dir)
                return corner, dirs
            # todo: change return type?
            i += inc