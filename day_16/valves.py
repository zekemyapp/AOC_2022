import re
import sys
import math
from tqdm import tqdm

MAX_TIME = 30  # PART_ONE
MAX_TIME = 26  # PART_TWO

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

class Player():
    def __init__(self, name, time_to_reach):
        self.name = name
        self.time_to_reach = time_to_reach

class FrontNodePachy():
    def __init__(self, name_a, name_b, parent):
        self.player_a = Player(name_a, 0)
        self.player_b = Player(name_b, 0)
        self.parent = parent
        self.visited = []
        self.time_of_visit = []
        self.time = 0

    def get_closest(self):
        if self.player_a.time_to_reach <= self.player_b.time_to_reach:
            return self.player_a
        else:
            return self.player_b

    def get_fartest(self):
        if self.player_a.time_to_reach <= self.player_b.time_to_reach:
            return self.player_b
        else:
            return self.player_a

# Breadth First Search
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

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

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
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

        if (node.time + (node.time_to_reach + 1)) >= MAX_TIME:
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

def solve_with_elephant():
    # Init frontier
    frontier = QueueFrontier()
    start_node = FrontNodePachy(START_POINT, START_POINT, None)
    frontier.add(start_node)

    best_so_far = 0

    results = []
    while True:
        # If nothing is empty, there is no solutionn
        if frontier.empty():
            return results 

        # Fetch new node to explore
        node = frontier.remove()

        closest_player = node.get_closest()
        fartest_player = node.get_fartest()
        if (node.time + (closest_player.time_to_reach + 1)) >= MAX_TIME:
            result = (node.time, node.visited, node.time_of_visit)
            results.append(result)
            calculate_result(results, True)
            continue

        # Solve closest and update fartest
        if closest_player.name == "AA":
            # Do not count first node
            time = node.time
            visited = [v for v in node.visited]
            time_of_visit = [t for t in node.time_of_visit]
        else:
            # Closest reach destination and open valve.
            # This time is free for the second player to perform actions
            time = node.time + closest_player.time_to_reach + 1
            fartest_player.time_to_reach -= closest_player.time_to_reach + 1

            # Copy arrays
            visited = [v for v in node.visited]
            time_of_visit = [t for t in node.time_of_visit]

            # Only closest arrived
            visited.append(closest_player.name)
            time_of_visit.append(time)

        # Check if it was over after this player reach its destination
        if len(visited) == len(all_valves_with_reward):
            result = (time, visited, time_of_visit)
            results.append(result)
            calculate_result(results, True)
            continue

        # #########################
        # if len(visited) >= (len(all_valves_with_reward) // 2):
        #     result = (time, visited, time_of_visit)
        #     test = calculate_result([result])
        #     if test >= best_so_far:
        #         best_so_far = test
        #     else:
        #         continue
        # #########################

        # print((time, frontier.size()))

        # Find next possible steps for closest player and reuse fartest
        added_new_closest = False
        for valve in all_valves_with_reward:
            # for each valve find all possible distances
            if valve in visited or valve == fartest_player.name:
                continue

            best_distance = all_distances[(closest_player.name, valve)]

            # Add to frontier
            new_node = FrontNodePachy(valve, fartest_player.name, node)
            # Global info
            new_node.time = time
            new_node.visited = visited
            new_node.time_of_visit = time_of_visit
            # Player info
            new_node.player_a.time_to_reach = best_distance
            new_node.player_b.time_to_reach = fartest_player.time_to_reach
            # Add to frontier
            frontier.add(new_node)
            added_new_closest = True

        if not added_new_closest:
            # No more nodes, only fartest left
            new_node = FrontNodePachy("AA", fartest_player.name, node)
            # Global info
            new_node.time = time
            new_node.visited = visited
            new_node.time_of_visit = time_of_visit
            # Player info
            new_node.player_a.time_to_reach = 99
            new_node.player_b.time_to_reach = fartest_player.time_to_reach
            # Add to frontier
            frontier.add(new_node)



def calculate_result(all_results, should_print=False):
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
            out += (MAX_TIME - _time) * all_valves_with_reward[_valve]

        all_outs.append(out)

    if should_print:
        print(f"PART_ONE = {max(all_outs)}") #1617
    return max(all_outs)

all_results = solve_with_elephant()
calculate_result(all_results, True)