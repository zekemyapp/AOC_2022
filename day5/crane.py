import re

# Read lines
lines = None
with open("input.txt") as file:
    lines = [line.strip("\n") for line in file]

# Separate stack lines from instructions
# An empty linne separates stack description from instructions
# Last line of stack descriptions is a guide to the position of
# the content
pos = 0
guide = None
instructions = 0
stack_lines = []
for line in lines:
    # An empty line separates stacks from instructions
    if len(line) == 0:
        guide = lines[pos-1]  # Last line before empty space
        instructions = lines[pos+1:]  # Line after empty space
        break
    if line[0] == '[':
        stack_lines.append(line)
    pos +=1

# Print initial state
print(guide)
for line in stack_lines:
    print(line)
print("\n")

# Get crates positions in lines usinng guide nnumber position
# these positions whill be the same on each on the stack lines
pos = 0
stack_guide = dict()
for c in guide:
    if guide[pos].isdigit():
        stack_guide[guide[pos]] = pos
    pos += 1

# Create stacks
stacks = dict()
for key in stack_guide:
    stacks[key] = []

# Fill stacks
while len(stack_lines) > 0:
    line = stack_lines.pop()
    for key in stack_guide:
        pos = stack_guide[key]
        if line[pos].isalpha():
            stacks[key].append(line[pos])

# Read instructions
def print_stacks():
    for key in stacks:
        print(stacks[key])
    print("\n")

print("Initial State:")
print_stacks()
for line in instructions:
    parsed = re.findall(r'\d+', line)
    sn = parsed[0]
    sfrom = parsed[1]
    sto = parsed[2]

    # PART 1
    # for i in range(int(sn)):
    #     crate = stacks[sfrom].pop()
    #     stacks[sto].append(crate)

    # PART 2
    inter_stack = []
    for i in range(int(sn)):
        crate = stacks[sfrom].pop()
        inter_stack.append(crate)
    for i in range(int(sn)):
        crate = inter_stack.pop()
        stacks[sto].append(crate)

    
print("Final State:")
print_stacks()