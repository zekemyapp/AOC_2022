import re

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def get_dir_char(dir):
    point = ">"
    if dir == RIGHT:
        point = ">"
    elif dir == DOWN:
        point = "v"
    elif dir == LEFT:
        point = "<"
    elif dir == UP:
        point = "^"
    return point

def get_first_point(line):
    for i in range(len(line)):
        if line[i] != " ":
            return i

def get_first_row_point(maze, col):
    for row in range(len(maze)):
        if len(maze[row]) > col:
            if maze[row][col] != " ":
                return row

def get_last_row_point(maze, col):
    first_row = get_first_row_point(maze, col)
    for row in range(first_row, len(maze)):
        if len(maze[row]) <= col:
            return row - 1
        
        if maze[row][col] == " ":
            return row - 1

    return len(maze) - 1


def print_maze(maze, start_point, direction):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            point = maze[row][col]
            if point == RIGHT:
                point = GREEN+">"+ENDC
            elif point == DOWN:
                point = GREEN+"v"+ENDC
            elif point == LEFT:
                point = GREEN+"<"+ENDC
            elif point == UP:
                point = GREEN+"^"+ENDC

            if row == start_point[0] and col == start_point[1]:
                point = RED+get_dir_char(direction)+ENDC

            print(point, end="")
        print("")

with open("input") as file:
    lines = [line.strip("\n").replace(":", "") for line in file]

maze_lines = []
inst = None
found = False
for line in lines:
    if found:
        inst = line
        break
    if len(line) == 0:
        found = True
        continue
    maze_lines.append([*line])

top_line = maze_lines[0]
start_point = None
direction = RIGHT
for i in range(len(top_line)):
    if top_line[i] == '.':
        start_point = (0, i)
        break

# maze_drawing = [[point for point in line] for line in maze_lines]
maze_lines[start_point[0]][start_point[1]] = direction

print(inst)
list_inst = re.split(r'(\d+)', inst)

for step in list_inst:
    if len(step) == 0:
        continue
    if step.isdigit():
        n = int(step)

        for i in range(n):
            if direction == RIGHT:
                row = start_point[0]
                col = start_point[1] + 1

                if col >= len(maze_lines[row]):
                    col = get_first_point(maze_lines[row])

                if maze_lines[row][col] == "#":
                    break

                start_point = (row, col)

            elif direction == DOWN:
                row = start_point[0] + 1
                col = start_point[1]

                if row > get_last_row_point(maze_lines, col):
                    row  = get_first_row_point(maze_lines, col)

                if maze_lines[row][col] == "#":
                    break

                start_point = (row, col)

            elif direction == LEFT:
                row = start_point[0]
                col = start_point[1] - 1

                if col < get_first_point(maze_lines[row]):
                    col = len(maze_lines[row]) - 1

                if maze_lines[row][col] == "#":
                    break

                start_point = (row, col)

            elif direction == UP:
                row = start_point[0] - 1
                col = start_point[1]

                if row < get_first_row_point(maze_lines, col):
                    row  = get_last_row_point(maze_lines, col)

                if maze_lines[row][col] == "#":
                    break

                start_point = (row, col)

            maze_lines[start_point[0]][start_point[1]] = direction
            # print_maze(maze_lines, start_point, direction)
            # input("")

    else:
        if len(step) > 1:
            print("THERE ARE DOUBLE LETTERS")

        if step == "R":
            direction += 1
            # Wrap
            if direction == 4:
                direction = 0
        elif step == "L":
            direction -= 1
            # Wrap
            if direction == -1:
                direction = 3
        
        maze_lines[start_point[0]][start_point[1]] = direction
        # print_maze(maze_lines, start_point, direction)
        # input("")

for row in range(len(maze_lines)):
    for col in range(len(maze_lines[row])):
        point = maze_lines[row][col]
        if point == RIGHT:
            point = GREEN+">"+ENDC
        elif point == DOWN:
            point = GREEN+"v"+ENDC
        elif point == LEFT:
            point = GREEN+"<"+ENDC
        elif point == UP:
            point = GREEN+"^"+ENDC

        if row == start_point[0] and col == start_point[1]:
            point = RED+get_dir_char(direction)+ENDC

        print(point, end="")
    print("")


result = (start_point[0]+1)*1000 + (start_point[1]+1)*4 + direction 
print(f"PART_ONE = {result}")  # 189140
