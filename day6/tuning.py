# Read input
BUFFER_SIZE = 14

lines = None
with open("input.txt") as file:
    lines = [line.strip("\n") for line in file]
input = lines[0]
input = [c for c in input]

def all_differ(buffer):
    return len(buffer) == len(set(buffer))

def insert_new(buffer, c):
    new_buffer = buffer[1:]
    new_buffer.append(c)
    return new_buffer

buffer = input[:BUFFER_SIZE]
count = BUFFER_SIZE
for c in input[BUFFER_SIZE:]:
    if all_differ(buffer):
        break

    buffer = insert_new(buffer, c)
    count += 1

print(count)