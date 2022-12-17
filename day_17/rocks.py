import numpy as np

ROCK_1 = [['#', '#', '#', '#']]
ROCK_2 = [['.', '#', '.'], ['#', '#', '#'], ['.', '#', '.']]
ROCK_3 = [['.', '.', '#'], ['.', '.', '#'], ['#', '#', '#']]
ROCK_4 = [['#'], ['#'], ['#'], ['#']]
ROCK_5 = [['#', '#'], ['#', '#']]

ROCKS = [
        ROCK_1,
        ROCK_2,
        ROCK_3,
        ROCK_4,
        ROCK_5
    ]

class RockCounter():
    def __init__(self):
        self.counter = -1

    def next_rock(self):
        self.counter += 1
        if self.counter >= len(ROCKS):
            self.counter = 0
        return ROCKS[self.counter]

def print_rock(rock):
    for i in range(len(rock)):
        for j in range(len(rock[i])):
            print(rock[i][j], end="")
        print("")

class Chamber():
    def __init__(self, size=0):
        self.grid = np.zeros((size,7), dtype=np.uint32)
        self.grid.fill(ord('.'))

        self.rock = None
        self.rock_pos = None

    def print(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                print(chr(self.grid[i][j]), end="")
            print("")
        print("")
    
    def grow_up(self, size):
        new_row = np.zeros((size, 7), dtype=np.uint32)
        new_row.fill(ord('.'))
        self.grid = np.vstack((new_row, self.grid))

    def print_with_rock(self):
        if self.rock is None:
            return

        new_array = self.grid.copy()
        rock = self.rock
        pos = self.rock_pos
        for i in range(len(rock)):
            for j in range(len(rock[i])):
                if rock[i][j] == '#':
                    new_array[i+pos[0]][j+pos[1]] = ord(rock[i][j])

        for i in range(len(new_array)):
            for j in range(len(new_array[i])):
                print(chr(new_array[i][j]), end="")
            print("")
        print("")

    def add_rock(self, rock):
        self.rock = rock
        self.rock_pos = (0, 2)
        self.grow_up(len(c_rock)+3)

    def rock_move_down(self):
        if self.rock is None:
            return

        rock = self.rock
        pos = self.rock_pos
        bottom_row_pos = self.rock_pos[0]+(len(rock)-1)

        # Check collision with bottom
        if bottom_row_pos+1 >= len(self.grid):
            self.rock_fix()
            return

        new_pos = (self.rock_pos[0]+1, self.rock_pos[1])
        new_bottom_row_pos = bottom_row_pos + 1

        # Check collision with any other piece
        n_rows = len(rock)
        n_cols = len(rock[0])
        for i in range(n_rows):
            for j in range(n_cols):
                obj = rock[len(rock)-1-i][j]
                grid_obj = self.grid[new_bottom_row_pos-i][new_pos[1]+j]
                grid_obj = chr(grid_obj)
                if obj == '#' and grid_obj != '.':
                    self.rock_fix()
                    return

        self.rock_pos = new_pos
    
    def rock_move_left(self):
        if self.rock is None:
            return
        if self.rock_pos[1]-1 < 0:
            return

        rock = self.rock
        pos = self.rock_pos
        new_pos = (self.rock_pos[0], self.rock_pos[1]-1)

        n_rows = len(rock)
        n_cols = len(rock[0])
        for j in range(n_cols):
            for i in range(n_rows):
                obj = rock[i][0+j]
                grid_obj = self.grid[new_pos[0]+i][new_pos[1]+j]
                grid_obj = chr(grid_obj)
                if obj == '#' and grid_obj != '.':
                    return

        self.rock_pos = new_pos

    def rock_move_right(self):
        if self.rock is None:
            return

        rock = self.rock
        pos = self.rock_pos
        right_col_pos = self.rock_pos[1]+(len(rock[0])-1)

        if right_col_pos+1 >= 7:
            return

        new_pos = (self.rock_pos[0], self.rock_pos[1]+1)
        new_right_col_pos = right_col_pos + 1

        n_rows = len(rock)
        n_cols = len(rock[0])
        # Check that none of the parts of the pieces will touch the ones in place 
        for j in range(n_cols):
            for i in range(n_rows):
                obj = rock[i][len(rock[0])-1-j]
                grid_obj = self.grid[new_pos[0]+i][new_right_col_pos-j]
                grid_obj = chr(grid_obj)
                if obj == '#' and grid_obj != '.':
                    return

        self.rock_pos = new_pos

    def rock_fix(self):
        rock = self.rock
        pos = self.rock_pos
        for i in range(len(rock)):
            for j in range(len(rock[i])):
                if rock[i][j] == '#':
                    self.grid[i+pos[0]][j+pos[1]] = ord('@') if rock[i][j] == '#' else ord('.')

        self.rock = None
        self.rock_pos = (0, 0)

rock_counter = RockCounter()
chamber = Chamber()

# c_rock = rock_counter.next_rock()
# c_rock = rock_counter.next_rock()
# c_rock = rock_counter.next_rock()


# chamber.add_rock(c_rock)

# chamber.add_rock(c_rock)
# chamber.rock_move_down()
# chamber.rock_move_down()
# chamber.rock_move_down()
# chamber.rock_move_down()
# chamber.rock_move_left()
# chamber.rock_move_left()
# chamber.rock_move_left()
# chamber.rock_move_right()
# chamber.rock_move_right()
# chamber.rock_move_right()
# chamber.rock_move_right()
# chamber.rock_fix()


# chamber.grow_up(1)
# chamber.add_rock(c_rock)
# chamber.rock_move_left()
# chamber.rock_move_left()
# chamber.rock_move_down()
# chamber.rock_move_down()
# chamber.rock_move_down()
# # chamber.rock_fix()

chamber.print_with_rock()
chamber.print()