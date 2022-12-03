
# Priorities definiton
# Each dictionary transpose the ascii value of their lowercase or uppercase equivalent
# to match the puzzle requirements. For example A = a - '0' and a = A - '0'
# Finally, the numbers miust be between 1 and 52, so also compensate for that. 
dict_a_z = {chr(ord('a')+(i-ord('A'))):i-ord('A')+1 for i in range(ord('A'), ord('Z')+1)}
dict_A_Z = {chr(ord('A')+(i-ord('a'))):i-ord('a')+1+26 for i in range(ord('a'), ord('z')+1)}
dict_all = dict_a_z | dict_A_Z

# Read lines
lines = None
with open("input.txt") as file:
    lines = [line.strip("\n") for line in file]

############
# PART 1: Find the common item between
# both half of a line.
############
result = 0
for rs in lines:
    n_items = len(rs)
    n_p = n_items // 2
    p1 = rs[:n_p]
    p2 = rs[n_p:]
    c = ''.join(set(p1).intersection(p2))
    result += dict_all[c]
print(f"first = {result}")

############
# PART 2: Find the common item between
# each three lines.
############
count = 0
result = 0
while count < (len(lines)-2):
    rs = [lines[count+i] for i in range(3)]
    c = ''.join(set(rs[0]).intersection(rs[1]))
    c = ''.join(set(c).intersection(rs[2]))
    result += dict_all[c]
    count += 3
print(f"second = {result}")


