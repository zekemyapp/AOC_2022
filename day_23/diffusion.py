import numpy as np
import time

RULES = ["north", "south", "west", "east"]
first_rule = 0

def update_marker(rule_marker):
    return (rule_marker+1) % 4

# Print Terrain
def print_terr(terrain):
    n_row, n_col = terrain.shape
    print(f"Printing with shape=({n_row},{n_col})")

    for row in range(n_row):
        for col in range(n_col):
            val = terrain[row][col]
            str_val = chr(val)
            print(str_val, end="")
        print("")

# Add a new row and col to every side
def expand_terr(terrain):
    n_row, n_col = terrain.shape

    new_row = np.zeros(shape=(1, n_col), dtype=np.int8)
    new_row.fill(ord("."))
    new_col = np.zeros(shape=(n_row+2, 1), dtype=np.int8)
    new_col.fill(ord("."))

    new_terrain = np.vstack([new_row, terrain])
    new_terrain = np.vstack([new_terrain, new_row])
    new_terrain = np.hstack([new_col, new_terrain])
    new_terrain = np.hstack([new_terrain, new_col])

    return new_terrain

def reduce_terr(terrain):
    n_row, n_col = terrain.shape

    lowest_col = n_col-1
    for row in range(n_row):
        for col in range(n_col):
            if terrain[row][col] == ord("#"):
                if col < lowest_col:
                    lowest_col = col
                continue

    highest_col = 0
    for row in range(n_row):
        for col in range(n_col-1, -1, -1):
            if terrain[row][col] == ord("#"):
                if col > highest_col:
                    highest_col = col
                continue

    lowest_row = n_row-1
    for col in range(n_col):
        for row in range(n_row):
            if terrain[row][col] == ord("#"):
                if row < lowest_row:
                    lowest_row = row
                continue

    highest_row = 0
    for col in range(n_col):
        for row in range(n_row-1, -1, -1):
            if terrain[row][col] == ord("#"):
                if row > highest_row:
                    highest_row = row
                continue

    new_terrain = np.delete(terrain,np.s_[highest_col+1:n_col],axis=1)
    new_terrain = np.delete(new_terrain,np.s_[0:lowest_col],axis=1)
    new_terrain = np.delete(new_terrain,np.s_[highest_row+1:n_row],axis=0)
    new_terrain = np.delete(new_terrain,np.s_[0:lowest_row],axis=0)
    return new_terrain

def count_space(terrain):
    n_row, n_col = terrain.shape

    counter = 0
    for row in range(n_row):
        for col in range(n_col):
            if terrain[row][col] == ord("."):
                counter += 1

    return counter

def get_adj(pos):
    NW = (pos[0]-1, pos[1]-1)
    N = (pos[0]-1, pos[1])
    NE = (pos[0]-1, pos[1]+1)
    W = (pos[0], pos[1]-1)
    E = (pos[0], pos[1]+1)
    SW = (pos[0]+1, pos[1]-1)
    S = (pos[0]+1, pos[1])
    SE = (pos[0]+1, pos[1]+1)

    return NW, N, NE, W, E, SW, S, SE


# Return True if there are adjacent elves
def check_adj(terrain, pos):
    NW, N, NE, W, E, SW, S, SE = get_adj(pos)
    all_adj = [NW, N, NE, W, E, SW, S, SE]

    for c_pos in all_adj:
        if terrain[c_pos[0]][c_pos[1]] == ord("#"):
            return True
    return False

# Return True if proposition is valid
def check_rule(terrain, pos, rule):
    NW, N, NE, W, E, SW, S, SE = get_adj(pos)

    if rule == "north":
        if (
            terrain[NW[0]][NW[1]] == ord(".")
            and terrain[N[0]][N[1]] == ord(".")
            and terrain[NE[0]][NE[1]] == ord(".")
        ):
            return True
    elif rule == "south":
        if (
            terrain[SW[0]][SW[1]] == ord(".")
            and terrain[S[0]][S[1]] == ord(".")
            and terrain[SE[0]][SE[1]] == ord(".")
        ):
            return True
    elif rule == "west":
        if (
            terrain[NW[0]][NW[1]] == ord(".")
            and terrain[W[0]][W[1]] == ord(".")
            and terrain[SW[0]][SW[1]] == ord(".")
        ):
            return True
    elif rule == "east":
        if (
            terrain[NE[0]][NE[1]] == ord(".")
            and terrain[E[0]][E[1]] == ord(".")
            and terrain[SE[0]][SE[1]] == ord(".")
        ):
            return True

    return False

def get_proposition(terrain, pos):
    NW, N, NE, W, E, SW, S, SE = get_adj(pos)
    current_rule = first_rule
    
    while True:
        rule = RULES[current_rule]
        if check_rule(terrain, pos, rule):
            if rule == "north":
                return N
            elif rule == "south":
                return S
            elif rule == "east":
                return E
            elif rule == "west":
                return W
            else:
                print(f"ERROR: tried to return invalid rule={current_rule}")
                return None

        current_rule = update_marker(current_rule)
        if current_rule == first_rule:
            return None

class Proposition():
    def __init__(self, prev_pos, next_pos):
        self.prev = prev_pos
        self.next = next_pos

    def __repr__(self):
        return f"{self.prev} -> {self.next}"

with open("input") as file:
    lines = [line.strip("\n") for line in file]

n_col = len(lines[0])
n_row = len(lines)

terrain = np.zeros(shape=(n_row, n_col), dtype=np.int8)
for row in range(len(lines)):
    for col in range(len(lines[0])):
        str_val = lines[row][col]
        terrain[row][col] = ord(str_val)

start_time = time.time()
# PART_ONE
# for i in range(10):
# PART_TWO
i = 0
while True:
    i += 1
    moved = False
    terrain = expand_terr(terrain)
    # print_terr(terrain)
    all_props = []
    n_row, n_col = terrain.shape
    for row in range(n_row):
        for col in range(n_col):
            if terrain[row][col] == ord("#"):
                # Calculate elf proposition
                elf_pos = (row, col)
                if check_adj(terrain, elf_pos):
                    new_pos = get_proposition(terrain, elf_pos)
                    if new_pos == None:
                        # print(f"elf at {elf_pos} proposes not moving")
                        continue
                    
                    # print(f"elf at {elf_pos} proposes moving to {new_pos}")
                    proposition = Proposition(elf_pos, new_pos)
                    all_props.append(proposition)
                else:
                    pass
                    # print(f"elf at {elf_pos} doesn't need to move")
    
    # print(f"time of proposition calculation = {time.time() - start_time} ")
    # start_time = time.time()

    while len(all_props) > 0:
        prop = all_props.pop()
        # Check if it is the only proposition with same
        # objective tile
        
        all_found = []
        for p in all_props:
            if prop.next == p.next:
                all_found.append(p)

        # print(f"for proposition {prop}, counter was {len(all_found)}")

        # TODO: This is supper inneficient cause we are counting several times
        # the same proposition. They could just be removed
        if len(all_found) == 0:
            moved = True
            terrain[prop.prev[0]][prop.prev[1]] = ord(".")
            terrain[prop.next[0]][prop.next[1]] = ord("#")
        else:
            for p in all_found:
                all_props.remove(p)


    first_rule = update_marker(first_rule)
    # print(f"time of proposition execution = {time.time() - start_time} ")
    # start_time = time.time()

    if not moved:
        break

    # input("")
    # print_terr(terrain)
    
terrain = reduce_terr(terrain)
print_terr(terrain)

print(f"PART_ONE={count_space(terrain)}")
print(f"PART_TWO={i}")
