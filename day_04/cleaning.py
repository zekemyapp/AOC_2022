# Read lines
lines = None
with open("input.txt") as file:
    lines = [line.strip("\n") for line in file]

############
# PART 1: Find sectionns that fully contain other sections.
# PART 2: Find all overlaping pairs.
############
result1 = 0
result2 = 0
for line in lines:
    sections = line.split(",")
    section1 = sections[0].split("-")
    section2 = sections[1].split("-")
    elf1 = [i for i in range(int(section1[0]), int(section1[1])+1)]
    elf2 = [i for i in range(int(section2[0]), int(section2[1])+1)]
    
    inter = set(elf1).intersection(elf2)
    if len(inter) > 0:
        result2 += 1
    if len(inter) == min(len(elf1), len(elf2)):
        result1 += 1

print(f"first = {result1}")
print(f"second = {result2}")