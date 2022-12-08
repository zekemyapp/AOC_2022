PRINT_GRID = False

lines = None
with open("input.txt") as file:
    lines = [line.strip("\n") for line in file]

grid = []
for line in lines:
    row = []
    for c in line:
        row.append(int(c))
    grid.append(row)

if PRINT_GRID:
    for row in grid:
        print(row)

COL_N = len(grid)
ROW_N = len(grid[0])

count = COL_N * 2
count += (ROW_N - 2) * 2
score = 0
for i in range(1, COL_N-1):
    for j in range(1, ROW_N-1):
        # Check up
        up = 0
        up_n = 0
        stop = False
        for x in range(i-1, -1, -1):  # Count backwards from i
            if grid[x][j] > up:
                up = grid[x][j]
            if not stop:
                up_n += 1
            if grid[x][j] >= grid[i][j]:
                stop = True

        # Check down
        down = 0
        down_n = 0
        stop = False
        for x in range(i+1, COL_N):  # Count forward to COL_N
            if grid[x][j] > down:
                down = grid[x][j]
            if not stop:
                down_n += 1
            if grid[x][j] >= grid[i][j]:
                stop = True
            
        # Check left
        left = 0
        left_n = 0
        stop = False
        for y in range(j-1, -1, -1):  # Count backwards from j
            if grid[i][y] > left:
                left = grid[i][y]
            if not stop:
                left_n += 1
            if grid[i][y] >= grid[i][j]:
                stop = True

        # Check lright
        right = 0
        right_n = 0
        stop = False
        for y in range(j+1, ROW_N):  # Count forward to ROW_N
            if grid[i][y] > right:
                right = grid[i][y]
            if not stop:
                right_n += 1
            if grid[i][y] >= grid[i][j]:
                stop = True

        n = grid[i][j]
        if up < n or down < n or left < n or right < n:
            count += 1

        local_score = up_n * down_n * left_n * right_n
        if local_score > score:
            score = local_score
    
print(f"PART ONE = {count}")
print(f"PART TWO = {score}")
