KEY = 811589153
N_MIXING = 10
PART_TWO  = True

from tqdm import tqdm

if PART_TWO:
    with open("input") as file:
        lines = [int(line.strip("\n")) * KEY for line in file]
else:
    with open("input") as file:
        lines = [int(line.strip("\n")) for line in file]

class Element():
    def __init__(self, index, val):
        self.idx = index
        self.val = val

    def __repr__(self):
        return f"({self.val})"

    def __str__(self):
        return f"({self.val})"

original = []
for i in range(len(lines)):
    original.append(Element(i, lines[i]))

output = [element for element in original]

def find_real_idx(mlist, idx):
    for i in range(len(mlist)):
        if mlist[i].idx == idx:
            return i

def find_zero(mlist):
    for i in range(len(mlist)):
        if mlist[i].val == 0:
            return i

print(output)
for i in tqdm(range(N_MIXING)):
    for e in original:
        if e.val == 0:
            continue

        current_idx = find_real_idx(output, e.idx)
        r_element = output.pop(current_idx)

        new_pos = current_idx+e.val
        # print(f"inserting in {current_idx} + {e.val} = {new_pos}")

        if new_pos == 0:
            output.append(r_element)
        elif abs(new_pos) > len(output):
            new_pos = new_pos % len(output)
            if new_pos == 0:
                output.append(r_element)
            else:
                output.insert(new_pos, r_element)
        else:
            output.insert(new_pos, r_element)
    # print(output)
    # input("")

# print(output)

val = 1000
zero_pos = find_zero(output)
val = (zero_pos + 1000) % len(output)
out = output[val].val
val = (zero_pos + 2000) % len(output)
out += output[val].val
val = (zero_pos + 3000) % len(output)
out += output[val].val

print(f"PART_ONE = {out}")