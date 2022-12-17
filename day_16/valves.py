import re
import sys
import math
from tqdm import tqdm

class Valve():
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.children = []

class FrontNode():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.visited = []
        self.time_of_visit = []
        self.time = 0
        self.time_to_reach = 0

# Breadth First Search
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_node(self, name):
        return any(node.name == name for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def size(self):
        return len(self.frontier)

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# Initialize
lines = None
with open("input") as file:
    lines = [line.strip("\n") for line in file]

all_valves = {}
all_valves_with_reward = {}

for line in lines:
    parsed = re.findall(r'[A-Z]{2}|\d+', line)
    name = parsed[0]
    rate = int(parsed[1])

    valve = Valve(name, rate)
    for i in range (2, len(parsed)):
        valve.children.append(parsed[i])
    all_valves[valve.name] = valve

    if valve.rate > 0:
        all_valves_with_reward[valve.name] = valve.rate

START_POINT = "AA"

# Find all paths to a node
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
        
        child_node = FrontNode(child, start_node)
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


# Precalculate all distances
print("Precomputing distances:")
all_distances = {}
all_valves_with_reward_keys = list(all_valves_with_reward.keys())
all_valves_with_reward_keys.append("AA")
for val_a in tqdm(all_valves_with_reward_keys):
    for val_b in tqdm(all_valves_with_reward_keys, leave=False):
        distances = find(FrontNode(val_a, None), val_b)
        # Find the shortest one
        best_distance = math.inf
        for dist in distances:
            steps = 0
            dist_node = dist
            while dist_node.parent is not None:
                dist_node = dist_node.parent
                steps += 1
            if steps < best_distance:
                best_distance = steps
        all_distances[(val_a, val_b)] = best_distance

def solve():
    # Init frontier
    frontier = StackFrontier()
    start_node = FrontNode(START_POINT, None)
    frontier.add(start_node)

    results = []
    while True:
        # If nothing is empty, there is no solutionn
        if frontier.empty():
            return results 

        # Fetch new node to explore
        node = frontier.remove()

        if (node.time + (node.time_to_reach + 1)) >= 30:
            result = (node.time, node.visited, node.time_of_visit)
            results.append(result)
            continue

        # Do not count first node
        if node.name != "AA":
            time = node.time + node.time_to_reach + 1
            visited = [v for v in node.visited]
            time_of_visit = [t for t in node.time_of_visit]
            visited.append(node.name)
            time_of_visit.append(time)
        else:
            time = node.time
            visited = [v for v in node.visited]
            time_of_visit = [t for t in node.time_of_visit]

        if len(visited) == len(all_valves_with_reward):
            result = (time, visited, time_of_visit)
            results.append(result)
            continue

        # print((time, frontier.size()))

        # Find next possible steps
        for valve in all_valves_with_reward:
            # for each valve find all possible distances
            if valve in visited:
                continue

            best_distance = all_distances[(node.name, valve)]

            # Add to frontier
            new_node = FrontNode(valve, node)
            new_node.time = time
            new_node.time_to_reach = best_distance
            new_node.visited = visited
            new_node.time_of_visit = time_of_visit
            frontier.add(new_node)

all_results = solve()
all_outs = []
for result in all_results:
    time = result[0]
    visited = result[1]
    time_of_visit = result[2]

    out = 0
    total_reward = 0
    for i in range(len(visited)):
        _valve = visited[i]
        _time = time_of_visit[i]
        total_reward += all_valves_with_reward[_valve]
        out += (30 - _time) * all_valves_with_reward[_valve]

    all_outs.append(out)

print(f"PART_ONE = {max(all_outs)}") #1617
