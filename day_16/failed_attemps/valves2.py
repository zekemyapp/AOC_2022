import re
import sys
import math

class Valve():
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.children = []

class Node():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

# class Node():
#     def __init__(self, name, cost, children):
#         self.name = name
#         self.cost = cost
#         self.children = children

# class Map():
#     def __init__(self, head):
#         self.head = head
#         self.children = set()

#     def add(self, name):
#         self.children.add(name)

#     def contains(self, name):
#         if name in self.children:
#             return True
#         return False

#     def find(self, name):
#         if not self.contains(name):
#             return None
        
#     # Should only be called if the name is in the tree
#     def _find(self, node, name):
#         if node.name == name:
#             return node
        
#         for child in node.children:
#             out = self._find(child, name)
#             if out is not None:
#                 return out
#         return None


lines = None
with open("input") as file:
    lines = [line.strip("\n") for line in file]

all_valves = {}
all_valves_with_reward = []

for line in lines:
    parsed = re.findall(r'[A-Z]{2}|\d+', line)
    name = parsed[0]
    rate = int(parsed[1])

    valve = Valve(name, rate)
    for i in range (2, len(parsed)):
        valve.children.append(parsed[i])
    all_valves[valve.name] = valve

    if valve.rate > 0:
        all_valves_with_reward.append(valve.name)

START_POINT = "AA"

def find(start_node, name, explored=None):
    if start_node.name == name:
        return [start_node]
    
    if explored is None:
        _explored = [start_node.name]
    else:
        _explored = [e for e in explored]

    results = []
    start_valve = all_valves[start_node.name]
    for child in start_valve.children:
        if child in _explored and child != name:
            # Went back in circles
            continue
        _explored.append(child)
        
        child_node = Node(child, start_node)
        result = find(child_node, name, _explored)

        if len(result) == 0:
            # Back road, ended up at the beginning at some point
            continue

        ############
        if explored is None:
            _explored = [start_node.name]
        else:
            _explored = [e for e in explored]
        ############
        results = results + result

    # None of the children reach the point
    return results

start_node = Node(START_POINT, None)
time = 0
rate_open = 0
pressure = 0

open_valves = []

# print(all_valves_with_reward)
# test_node = Node("BB", None)
# test = find(test_node, "JJ")
# for t in test:
#     steps = 0
#     node = t
#     while node.parent is not None:
#         print(node.name)
#         node = node.parent
#         steps += 1
#     print(steps)
# sys.exit()

while len(open_valves) < len(all_valves_with_reward):
    heur = {}
    for valve in all_valves:
        if valve == start_node.name or valve in open_valves:
            continue
        all_dist = find(start_node, valve)

        best = 99999
        best_node = None
        for dist in all_dist:
            steps = 0
            node = dist
            while node.parent is not None:
                    node = node.parent
                    steps += 1
            if steps < best:
                best = steps
                best_node = dist

        reward = math.ceil(all_valves[valve].rate / (best*best))
        heur[valve] = (reward, best, best_node)
    # print(heur)

    best = -99
    best_valve = None
    best_steps = 99999
    best_path = None
    for h in heur:
        if heur[h][0] > best or (heur[h][0] == best and heur[h][1] < best_steps):
        # if heur[h][1] < best_steps:
            best = heur[h][0]
            best_valve = h
            best_steps = heur[h][1]
            best_path = heur[h][2]
    
    if (time + best_steps + 1) > 30:
        break

    time += best_steps + 1
    # time += 1
    
    pressure += rate_open * (best_steps + 1)
    rate_open += all_valves[best_valve].rate
    start_node = Node(best_valve, None)
    open_valves.append(best_valve)

    print(f"NEW STATE: time={time}; rate={rate_open}; room={start_node.name}; pressure={pressure}")

pressure += (30-time) * rate_open

print(f"FINAL PRESSURE = {pressure}") #1728



