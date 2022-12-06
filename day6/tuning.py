# Read input
lines = None
with open("input.txt") as file:
    lines = [line.strip("\n") for line in file]
input = lines[0]
input = [c for c in input]

buffer = input[:4]
count = 4

def all_differ():
    if (
        buffer[0] != buffer[1] and
        buffer[0] != buffer[2] and
        buffer[0] != buffer[3] and
        buffer[1] != buffer[2] and
        buffer[1] != buffer[3] and
        buffer[2] != buffer[3]
    ):
        return True
    return False

def insert_new(c):
    buffer[0] = buffer[1]
    buffer[1] = buffer[2]
    buffer[2] = buffer[3]
    buffer[3] = c

for c in input[4:]:
    if all_differ():
        break

    insert_new(c)
    count += 1

print(count)