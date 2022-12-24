import numpy as np
from tqdm import tqdm

N_ROCKS = 2022  # PART ONE
N_ROCKS = 1000000000000  # PART TWO

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
        self.rock_number = 0

        self.saved_height = 0

        self.next_stop = 0
        self.cpy_array = None

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

        piece_size = len(c_rock)+3
        n_rows, n_cols = self.grid.shape

        # Empty grid, just grow it to needed size
        if n_rows == 0:
            self.grow_up(piece_size)
            return

        # Get highest point in the grid
        highest = None
        for i in range(n_rows):
            for j in range(n_cols):
                if self.grid[i][j] != ord('.'):
                    highest = (i, j)
                    break
            if highest is not None:
                    break

        # There are no pieces in the grid
        if highest is None:
            needed_space = piece_size - n_rows
            if needed_space > 0:
                self.grow_up(needed_space)
            return

        # add new needed space
        needed_space = piece_size - highest[0]
        if needed_space >= 0:
            self.grow_up(needed_space) 
        else:
            # reshape to remove extra space
            self.grid = self.grid[abs(needed_space):]


    def rock_move_down(self):
        if self.rock is None:
            return False

        rock = self.rock
        pos = self.rock_pos
        bottom_row_pos = self.rock_pos[0]+(len(rock)-1)

        # Check collision with bottom
        if bottom_row_pos+1 >= len(self.grid):
            self.rock_fix()
            return False

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
        return True
    
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
        if self.rock is None:
            return

        rock = self.rock
        pos = self.rock_pos
        for i in range(len(rock)):
            for j in range(len(rock[i])):
                if rock[i][j] == '#':
                    self.grid[i+pos[0]][j+pos[1]] = ord('@') if rock[i][j] == '#' else ord('.')

        self.rock = None
        self.rock_pos = (0, 0)
        self.rock_number += 1

    def is_rock_empty(self):
        return (self.rock is None)

    def get_rock_count(self):
        return self.rock_number

    def get_highest(self):
        n_rows, n_cols = self.grid.shape

        # Empty grid, just grow it to needed size
        if n_rows == 0:
            return 0

        highest = None
        for i in range(n_rows):
            for j in range(n_cols):
                if self.grid[i][j] != ord('.'):
                    highest = (i, j)
                    break
            if highest is not None:
                    break
        if highest is None:
            return 0
        return highest[0]


    def get_height(self):
        n_rows, n_cols = self.grid.shape

        # Empty grid, just grow it to needed size
        if n_rows == 0:
            return 0

        highest = None
        for i in range(n_rows):
            for j in range(n_cols):
                if self.grid[i][j] != ord('.'):
                    highest = (i, j)
                    break
            if highest is not None:
                    break
        if highest is None:
            return 0
        return n_rows - highest[0]

    def optimize(self):
        self.grid = self.grid[:-50]
        self.saved_height += 50

    def check_patter(self):
        if self.rock_number < 5:
            return

        highest = self.get_highest()
        new_array = self.grid[highest:]

        if self.cpy_array is None:
            self.cpy_array = np.vstack((new_array, new_array))
            self.next_stop = self.rock_number*2

        if np.array_equal(new_array, self.cpy_array):
            print(f"FOUND SOMETHING AT: {self.rock_number}")
        else:
            self.cpy_array = np.vstack((new_array, new_array))
            self.next_stop = self.rock_number*2

rock_counter = RockCounter()
chamber = Chamber()

with open("sample") as file:
    lines = [line.strip("\n") for line in file]

line = lines[0]
pattern_len = len(line)
print(f"There will be {pattern_len} steps")

pbar = tqdm(total=N_ROCKS)
pattern_step = 0
while True:
    _step = pattern_step % pattern_len
    step = line[_step]

    if chamber.is_rock_empty():
        # Game is finished
        if chamber.get_rock_count() == N_ROCKS:
            break

        # if chamber.get_height() > 100:
        #     chamber.optimize()
        chamber.check_patter()
        
        pbar.update(1)
        c_rock = rock_counter.next_rock()
        chamber.add_rock(c_rock)

    # chamber.print_with_rock()
    # input("")
    
    if step == '>':
        chamber.rock_move_right()
    elif step == '<':
        chamber.rock_move_left()

    chamber.rock_move_down()

    pattern_step += 1    
pbar.close()

height = chamber.get_height()
height += chamber.saved_height 
print(f"Result = {height}")