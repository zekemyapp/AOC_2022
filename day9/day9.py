import numpy as np

PART_TWO = True
lines = None
with open("input") as file:
    lines = [line.strip("\n") for line in file]

class Grid():
    def __init__(self):
        self.grid = np.zeros((2,2))

    def get_row_size(self):
        n_rows,_ = self.grid.shape
        return n_rows

    def get_count(self):
        count = 0
        for row in self.grid:
            for n in row:
                if n: count += 1
        return count

    def set_point(self, pos):
        self.grid[pos[0]][pos[1]] = 1

    def get_col_size(self):
        _,n_cols = self.grid.shape
        return n_cols

    def grow_right(self):
        new_col = np.zeros((self.get_row_size(),1))
        self.grid = np.hstack((self.grid, new_col))

    def grow_left(self):
        new_col = np.zeros((self.get_row_size(),1))
        self.grid = np.hstack((new_col, self.grid))

    def grow_up(self):
        new_row = np.zeros((1,self.get_col_size()))
        self.grid = np.vstack((new_row, self.grid))

    def grow_down(self):
        new_row = np.zeros((1,self.get_col_size()))
        self.grid = np.vstack((self.grid, new_row))

grid = Grid()
h = (0,0)
t = (0,0)
knots = [(0,0) for i in range(9)]

def move_node(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]

    # Square distance b from a
    if x*x + y*y <= 2:
        return b

    if x > 0:
        b = (b[0]+1, b[1])
    elif x < 0:
        b = (b[0]-1, b[1])

    if y > 0:
        b = (b[0], b[1]+1)
    elif y < 0:
        b = (b[0], b[1]-1)
    return b

def move_up():
    global grid, h, t, knots
    if h[0] == 0:
        grid.grow_up()
        t = (t[0]+1, t[1])
        for i in range(len(knots)):
            knots[i] = (knots[i][0]+1, knots[i][1])
    else:
        h = (h[0]-1, h[1])

def move_down():
    global grid, h, t
    if h[0]+1 == grid.get_row_size():
        grid.grow_down()
    h = (h[0]+1, h[1])

def move_left():
    global grid, h, t
    if h[1] == 0:
        grid.grow_left()
        t = (t[0], t[1]+1)
        for i in range(len(knots)):
            knots[i] = (knots[i][0], knots[i][1]+1)
    else:
        h = (h[0], h[1]-1)

def move_right():
    global grid, h, t
    if h[1]+1 == grid.get_col_size():
        grid.grow_right()
    h = (h[0], h[1]+1)

for line in lines:
    input = line.split()
    dir = input[0]
    steps = int(input[1])

    for step in range(steps):
        # print(f"moving {dir}")
        if dir == 'U':
            move_up()
        elif dir == 'D':
            move_down()
        elif dir == 'L':
            move_left()
        elif dir == 'R':
            move_right()
        else:
            print("WRONG MOVEMENT")

        # print(f"before h={h} t={t}")
        t = move_node(h, t)
        # print(f"after h={h} t={t}")

        knots[0] = move_node(h,knots[0])
        for i in range(len(knots)-1):
            knots[i+1] = move_node(knots[i],knots[i+1])
        
        # Update Grid
        if PART_TWO:
            grid.set_point(knots[8])
        else:
            grid.set_point(t)

if PART_TWO:
    print(f"PART TWO = {grid.get_count()}")
else:
    print(f"PART ONE = {grid.get_count()}")