import os
import time

PART_TWO = True

lines = None
with open("input") as file:
    lines = [line.strip("\n") for line in file]

class Node():
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.steps = steps

# Breadth First Search
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# Depth First Search (Works best for this maze)
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

# Build maze
n_row = len(lines)
n_col = len(lines[0])
maze = []
for _row in lines:
    row = []
    for col in _row:
        row.append(col)
    maze.append(row)

# For path display
visited = [[False for _ in range(n_col)] for _ in range(n_row)]
steps = 0

start = None
pos = None
goal = None

def get_content(pos):
    out = maze[pos[0]][pos[1]]
    if out == 'S':
        out = 'a'
    elif out == 'E':
        out = 'z'
    return out

def get_options(pos):
    up = (pos[0]-1, pos[1]) if pos[0]-1 >= 0 else None
    down = (pos[0]+1, pos[1]) if pos[0]+1 < n_row else None
    left = (pos[0], pos[1]-1) if pos[1]-1 >= 0 else None
    right = (pos[0], pos[1]+1) if pos[1]+1 < n_col else None

    current = get_content(pos)
    options = []

    for direction in [up, down, left, right]:
        if direction is not None:
            val = get_content(direction)
            if ord(val) <= ord(current)+1:
                options.append(direction)

    return options

class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

def print_maze():
    os.system("clear")
    for i in range(n_row):
        for j in range(n_col):
            char_color = colors.GREEN if visited[i][j] else colors.RED
            print(f"{char_color}{maze[i][j]}{colors.END}", end="")
        print("")

def solve_maze(start, goal):
    global visited, steps
    visited = [[False for _ in range(n_col)] for _ in range(n_row)]
    visited[start[0]][start[1]] = True

    # Init frontier
    frontier = QueueFrontier()
    frontier.add(Node(state=start, parent=None))
    explored = set()

    while True:
        # If nothing is empty, there is no solutionn
        if frontier.empty():
            return False

        # Fetch new node to explore
        node = frontier.remove()

        # Check if goal was reached
        if node.state == goal:
            while node.parent is not None:
                visited[node.state[0]][node.state[1]] = True
                node = node.parent
                steps += 1
            return True

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for state in get_options(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node)
                frontier.add(child)


#################
# Execution
################

# Find start and end
for i in range(n_row):
    for j in range(n_col):
        if maze[i][j] == 'S':
            start = (i, j)
        if maze[i][j] == 'E':
            goal = (i,j)

if not PART_TWO:
    solve_maze(start, goal)
    print_maze()
    print(f"PART_ONE = {steps}")
else:
    options = []
    for i in range(n_row):
        for j in range(n_col):
            if maze[i][j] == 'a':
                options.append((i,j))
    min_steps = 1000
    for op in options:
        steps = 0
        solved = solve_maze(op, goal)
        if solved and steps < min_steps:
            print_maze()
            min_steps = steps
    print(f"PART_TWO = {min_steps}")