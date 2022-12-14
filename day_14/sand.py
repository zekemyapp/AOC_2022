lines = None
with open("input") as file:
    lines = [line.strip("\n") for line in file]

PART_TWO = False

min_x = 600
max_x = 0
min_y = 600
max_y = 0
maze_input = []

for line in lines:
    line = line.replace(" ", "").split("->")
    wall = []
    for point in line:
        point = point.split(",")
        point = (int(point[0]), int(point[1]))
        wall.append(point)

        # Get maze limits
        min_x = min(min_x, point[0])
        max_x = max(max_x, point[0])
        min_y = min(min_y, point[1])
        max_y = max(max_y, point[1])
    maze_input.append(wall)

print(f"maze limits: {min_x},{min_y} -> {max_x},{max_y}")

# Add sand genneratinng point
point = (500, 0)
min_x = min(min_x, point[0])
max_x = max(max_x, point[0])
min_y = min(min_y, point[1])
max_y = max(max_y, point[1])

# Calculate maze shape
n_y = max_y-min_y+1
n_x = max_x-min_x+1

if PART_TWO:
    max_y += 2
    n_y += 2
    min_x = min_x - n_y
    max_x = max_x + n_y
    n_x = max_x-min_x+1
    wall = [(min_x, max_y), (max_x, max_y)]
    maze_input.append(wall)

start_point = (500-min_x, 0-min_y)
maze = [["." for j in range(n_y)] for i in range(n_x)]

def print_maze():
    for j in range(n_y):
        for i in range(n_x):
            print(maze[i][j], end="")
        print("")

def print_maze_step(grain):
    for j in range(n_y):
        for i in range(n_x):
            if (i,j) == grain:
                print("o", end="")
            else:
                print(maze[i][j], end="")
        print("")

# Initialize maze
maze[start_point[0]][start_point[1]] = '+'
for wall in maze_input:
        prev_point = None
        for point in wall:
            if prev_point is None:
                maze[point[0]-min_x][point[1]-min_y] = '#'
                prev_point = point
                continue
            
            if point[0] == prev_point[0]:
                sign = 1 if point[1] > prev_point[1] else -1
                for j in range(prev_point[1]+sign, point[1]+sign, sign):
                    maze[point[0]-min_x][j-min_y] = '#'
                prev_point = point

            elif point[1] == prev_point[1]:
                sign = 1 if point[0] > prev_point[0] else -1
                for i in range(prev_point[0]+sign, point[0]+sign, sign):
                    maze[i-min_x][point[1]-min_y] = '#'
                prev_point = point

def roll_grain(grain):
    global maze

    if maze[start_point[0]][start_point[1]] == 'o':
        # Maze is full, no sand is falling
        return False

    while True:
        #print_maze_step(grain)
        if grain[1]+1 >= n_y:
            return False

        elif maze[grain[0]][grain[1]+1] == '.':
            grain = (grain[0], grain[1]+1)
            continue

        elif grain[0]-1 < 0:
            return False

        elif maze[grain[0]-1][grain[1]+1] == '.':
            grain = (grain[0]-1, grain[1]+1)
            continue

        elif grain[0]+1 >= n_x:
            return False

        elif maze[grain[0]+1][grain[1]+1] == '.':
            grain = (grain[0]+1, grain[1]+1)
            continue

        else:
            maze[grain[0]][grain[1]] = 'o'
            return True


count = 0
while True:
    grain = start_point

    if roll_grain(grain):
        count += 1
        continue
    else:
        break

if not PART_TWO:
    print_maze()
    print(f"PART_ONE = {count}")
else:
    print(f"PART_TWO = {count}")