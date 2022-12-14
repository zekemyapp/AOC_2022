import ast
import sys


def compare (left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif left > right:
            return -1
        else:
            return 0

    if isinstance(left, list) and isinstance(right, list):
        if len(left) == 0 and len(right) == 0:
            return 0
        if len(left) > 0 and len(right) == 0:
            return -1
        if len(left) == 0 and len(right) > 0:
            return 1
        
        x = compare(left[0], right[0])
        if (x != 0):
            return x

        return compare(left[1:], right[1:])

    if isinstance(left, int) and isinstance(right, list):
        new_list = [left]
        return compare(new_list, right)
    
    if isinstance(left, list) and isinstance(right, int):
        new_list = [right]
        return compare(left, new_list)

# Not the quickest, but the easier to remember :)
def sort(array):
    n = len(array)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if compare(array[j], array[j+1]) == -1:
                swapped = True
                array[j], array[j + 1] = array[j + 1], array[j]
         
        if not swapped:
            return

lines = None
with open("input") as file:
    lines = [line.strip("\n") for line in file]

pairs = []
packages = []
packages.append([[2]])
packages.append([[6]])

for i in range(0, len(lines), 3):
    left = ast.literal_eval(lines[i])
    right = ast.literal_eval(lines[i+1])

    # Check if they are in the right order
    if compare(left, right) == 1:
        # Append pair index
        pairs.append(i//3 + 1)

    packages.append(left)
    packages.append(right)

print(f"PART_ONE = {sum(pairs)}")

sort(packages)
out = 1
for i in range(len(packages)):
    if packages[i] == [[2]]:
        out *= i+1
    if packages[i] == [[6]]:
        out *= i+1
print(f"PART_TWO = {out}")