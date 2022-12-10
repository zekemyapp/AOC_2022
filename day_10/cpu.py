lines = None
with open("input") as file:
    lines = [line.strip("\n") for line in file]

def check_X(cycle, X):
    ss = cycle*X
    if cycle in [20, 60, 100, 140, 180, 220]:
        print(f"[{cycle}]: {X}, {ss}")
        return ss
    return 0

def check_pixel(cycle, X):
    global grid
    pixel = (cycle-1)%40
    if (X-1 == pixel or
        X == pixel or
        X+1 == pixel):
        grid[cycle-1] = 1


cpu_cycle = 1
X = 1
current_cmd = "noop"
count = 0

length = 40 * 6
grid = [0 for i in range(length)]

check_pixel(cpu_cycle, X)

for line in lines:
    input = line.split()
    cmd = input[0]
    if cmd == "addx":
        val = input[1]

    if cmd == "noop":
        cpu_cycle +=1
        count += check_X(cpu_cycle, X)
        check_pixel(cpu_cycle, X)

    elif cmd == "addx":
        cpu_cycle +=1
        count += check_X(cpu_cycle, X)
        pixel = (cpu_cycle-1)%40
        check_pixel(cpu_cycle, X)

        cpu_cycle +=1
        X += int(val)
        count += check_X(cpu_cycle, X)
        check_pixel(cpu_cycle, X)

print(f"PART ONE = {count}")
print(f"PART TWO")

def print_crt(grid):
    for i in range(length):
        if i%40 == 0:
            print("\n", end="")
        if not grid[i]:
            print('.', end="")
        else:
            print('#', end="")
    print("\n", end="")

print_crt(grid)