import re
from tqdm import tqdm

lines = None
with open("input") as file:
    lines = [line.strip("\n") for line in file]

# Use ridiculously high and low numbers to find min-max
min_x = 99999999999
max_x = -99999999999
min_y = 99999999999
max_y = -99999999999
sensors = {}

for line in lines:
        parsed = re.findall(r'[-]?\d+', line)
        sensor = (int(parsed[0]), int(parsed[1]))
        beacon = (int(parsed[2]), int(parsed[3]))

        min_x = min(min_x, sensor[0], beacon[0])
        max_x = max(max_x, sensor[0], beacon[0])
        min_y = min(min_y, sensor[1], beacon[1])
        max_y = max(max_y, sensor[1], beacon[1])

        sensors[sensor] = beacon

# Find biggest manhattan distance to grow the array
# The right amount
biggest = 0
all_mhd = {}
for sensor in sensors:
        beacon = sensors[sensor]
        dy = beacon[1] - sensor[1]
        dx = beacon[0] - sensor[0]
        mhd = abs(dx) + abs(dy)
        if mhd > biggest:
            biggest = mhd
        all_mhd[sensor] = mhd

print(f"grid limits: {min_x},{min_y} -> {max_x},{max_y}")
min_x -= mhd
max_x += mhd
print(f"grid limits with compensation: {min_x},{min_y} -> {max_x},{max_y}")

def print_row():
        for i in range(len(Y)):
                print(Y[i], end="")
        print("")

def tun_freq(x, y):
    return x*4000000+y

def fill_manhattan_distance(Y, row, point, distance, min, max):
    for i in tqdm(range(min, max+1), leave=False):
        if abs(i - point[0]) + abs(row - point[1]) <= distance:
            if Y[i-min] == '.':
                Y[i-min] = '#'
    return Y

def fill_row(Y, row, min, max):
    for sensor in sensors:
            if sensor[1] == row and sensor[0] >= min and sensor[0] <= max:
                    Y[sensor[0]-min] = 'S'

            beacon = sensors[sensor]
            if beacon[1] == row and beacon[0] >= min and beacon[0] <= max:
                    Y[beacon[0]-min] = 'B'

            dy = beacon[1] - sensor[1]
            dx = beacon[0] - sensor[0]

            mhd = abs(dx) + abs(dy)

            Y = fill_manhattan_distance(Y, row, sensor, mhd, min, max)
    return Y


#################
# PART ONE
#################
row = 10
row = 2000000
Y = ['.' for i in range(max_x-min_x+1)]
Y = fill_row(Y, row, min_x, max_x)

count = 0
for c in Y:
    if c == "#":
        count += 1
# print_row()
print(f"PART_ONE = {count}") # 4919281

#################
# PART TWO
#################

def get_border(point, mhd, lower_limit, upper_limit):
    min_x = point[0] - mhd
    max_x = point[0] + mhd
    min_y = point[1] - mhd
    max_y = point[1] + mhd

    border = set()
    counter = range(0, mhd+1)
    for i in tqdm(counter, leave=False):
        _x = i
        _y = mhd-i

        x = point[0]+_x
        y = point[1]+_y
        if (x <= upper_limit and x >= lower_limit and
            y <= upper_limit and y >= lower_limit):
            border.add((x,y))

        x = point[0]+_x
        y = point[1]-_y
        if (x <= upper_limit and x >= lower_limit and
            y <= upper_limit and y >= lower_limit):
            border.add((x,y))

        x = point[0]-_x
        y = point[1]+_y
        if (x <= upper_limit and x >= lower_limit and
            y <= upper_limit and y >= lower_limit):
            border.add((x,y))

        x = point[0]-_x
        y = point[1]-_y
        if (x <= upper_limit and x >= lower_limit and
            y <= upper_limit and y >= lower_limit):
            border.add((x,y))

    return border


all_borders = set()
for sensor in tqdm(sensors):
    beacon = sensors[sensor]
    dy = beacon[1] - sensor[1]
    dx = beacon[0] - sensor[0]
    mhd = abs(dx) + abs(dy)

    all_borders.update(get_border(sensor, mhd+1, 0, 4000000))

print("Brute Forcing PART_TWO")
for point in tqdm(all_borders):
    found = False
    for sensor in sensors:
        beacon = sensors[sensor]
        dy = beacon[1] - sensor[1]
        dx = beacon[0] - sensor[0]
        mhd = abs(dx) + abs(dy)
        if abs(point[0] - sensor[0]) + abs(point[1] - sensor[1]) <= mhd:
            found  = True

    if not found:
        print(f"found ({point[0]}, {point[1]}) = {tun_freq(point[0], point[1])}")
