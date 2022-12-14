lines = None
with open("sample") as file:
    lines = [line.strip("\n") for line in file]

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
maze = [["." for j in range(n_y)] for i in range(n_x)]

def print_maze():
    for j in range(n_y):
        for i in range(n_x):
            print(maze[i][j], end="")
        print("")

# Initialize maze
for wall in maze_input:
        for point in wall:
            maze[point[0]-min_x][point[1]-min_y] = '#'
            

print_maze()