import sys
from os import system

SAMPLE = False
if SAMPLE:
    FILE = "sample2"
    LIMIT = 30
else:
    FILE = "input"
    LIMIT = 328

class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


class Node():
    def __init__(self, player, t, parent):
        self.player = player
        self.time = t
        self.parent = parent

# Breadth First Search
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, player, t):
        return any(
            (node.player == player and node.time == t) for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

DIRECTION = {
    ">": 0,
    "v": 1,
    "<": 2,
    "^": 3
}

with open(FILE) as file:
    lines = [line.strip("\n") for line in file]

n_col = len(lines[0])
n_row = len(lines)
start_pos = (0, 1)
end_pos = (n_row-1, n_col-2)

blizzard_stack = []
for row in range(n_row):
    for col in range(n_col):
        if lines[row][col] in DIRECTION:            
            blizzard_stack.append((row, col, lines[row][col]))

def print_terr(blizzard, player, visited=[]):
    system('clear')
    for row in range(n_row):
        for col in range(n_col):
            pos_tuple = (row, col)
            char_color = colors.GREEN if (pos_tuple in visited) else colors.RED

            if (row, col) == player:
                char_char = "E"
            elif (
                (row == 0 and col != start_pos[1])
                or (row == n_row-1 and col != end_pos[1])
                or col == 0
                or col == n_col-1
            ):
                char_char = "#"
            elif pos_tuple in blizzard:
                if blizzard[pos_tuple][1] > 1:
                    char_char = blizzard[pos_tuple][1]
                else:
                    char_char = blizzard[pos_tuple][0]
            else:
                char_char = "."
            print(f"{char_color}{char_char}{colors.END}", end="")
        print("")

def solve_blizzard(t):
    result = {}

    for wind in blizzard_stack:
        wind_row = wind[0]
        wind_col = wind[1]
        wind_dir = wind[2]

        if wind_dir == ">":
            wind_col = wind_col - 1 + t
            wind_col = (wind_col % (n_col-2)) + 1
        elif wind_dir == "v":
            wind_row = wind_row - 1 + t
            wind_row = (wind_row % (n_row-2)) + 1
        elif wind_dir == "<":
            wind_col = wind_col - 1 - t
            wind_col = (wind_col % (n_col-2))
            if wind_col < 0:
                wind_col += (n_col-2)
            wind_col += 1
        elif wind_dir == "^":
            wind_row = wind_row - 1 - t
            wind_row = (wind_row % (n_row-2))
            if wind_row < 0:
                wind_row += (n_row-2)
            wind_row += 1
        else:
            print(f"ERROR 2")
            sys.exit()

        if (wind_row, wind_col) in result:
            result[(wind_row, wind_col)] = (
                wind_dir, result[(wind_row, wind_col)][1] + 1)
        else:
            result[(wind_row, wind_col)] = (wind_dir, 1)

    return result

def mhd(a, b):
    return abs(b[0]- a[0]) + abs(b[1]- a[1])

def get_adj(pos):
    N = (pos[0]-1, pos[1])
    W = (pos[0], pos[1]-1)
    E = (pos[0], pos[1]+1)
    S = (pos[0]+1, pos[1])
    return N, W, E, S


def solve_maze(start_point, end_point, offset_time):
    # Init frontier
    frontier = StackFrontier()
    frontier.add(Node(start_point, offset_time, None))
    explored = set()
    results = []

    while True:
        # If frontier is empty, there is no solutionn
        if frontier.empty():
            print("NO SOLUTION FOUND")
            return results

        # Fetch new node to explore
        node = frontier.remove()

        # Check if goal was reached
        if node.player == end_point:
            count = 0
            while node.parent is not None:
                node = node.parent
                count += 1
            results.append(count)
            continue
        else:
            pass

        # Mark node as explored
        explored.add((node.player, node.time))

        # PRUNE 1
        if (node.time - offset_time) >= LIMIT:
            continue

        # Calculate step of grid
        N, W, E, S = get_adj(node.player)    
        blizzard = solve_blizzard(node.time+1)

        options = [N, W, E, S, node.player]
        valid_position = []

        for option in options:
            if (
                (option[0] <= 0 and option != start_pos) # 
                or (option[0] >= n_row-1 and option != end_pos)
                or option[1] <= 0
                or option[1] >= n_col-1
                or option in blizzard
                # or option in node.failed
            ):
                continue
            valid_position.append(option)

        if len(valid_position) > 0:
            # print(f"PLAYER OPTIONS = {len(valid_position)}")
            # move = (-2, -2)
            # for p in valid_position:
            #     if mhd(p, end_pos) < mhd(move, end_pos):
            #         move = p

            # Add neighbors to frontier
            new_time = node.time+1
            for move in valid_position:
                if not frontier.contains_state(move, new_time) and (move, new_time) not in explored:
                    child = Node(player=move, t=new_time, parent=node)
                    frontier.add(child)
            continue
        else:
            continue

min_time = 0
results = solve_maze(start_pos, end_pos, 0)

if len(results) > 0:
    print(results)
    min_time = min(results)
    print(f"PART_ONE = {min(results)}")
else:
    print(f"ERROR 1")
    sys.exit()
# 328 too high

results = solve_maze(end_pos, start_pos, min_time)

if len(results) > 0:
    print(results)
    min_time += min(results)
    print(f"PART_TWO_ONE = {min(results)}")
else:
    print(f"ERROR 2")
    sys.exit()

results = solve_maze(start_pos, end_pos, min_time)

if len(results) > 0:
    print(results)
    min_time += min(results)
    print(f"PART_TWO_TWO = {min(results)}")
else:
    print(f"ERROR 3")
    sys.exit()


print(f"PART_TOTAL = {min_time}")