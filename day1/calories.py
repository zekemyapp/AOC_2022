lines = None
with open("calories_input.txt") as file:
    lines = [line.strip("\n") for line in file]

elves = []
current_count = 0
for line in lines:
    if len(line) == 0:
        elves.append(current_count)
        current_count = 0
    else:
        current_count += int(line)

first = 0
second = 0
third = 0

for item in elves:
    if item >= first:
        third = second
        second = first
        first = item
    elif item >= second:
        third = second
        second = item
    elif item > third:
        third = item

print(f"first elf: {first}")
print(f"second elf: {second}")
print(f"third elf: {third}")
print(f"top three: {first+second+third}")