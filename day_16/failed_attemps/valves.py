import re
import sys

class Node():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.time = 30
        self.explored = set()
        self.rate = 0
        self.pressure = 0

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

# Depth First Search (Works best for this maze)
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Valve():
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.children = set()

    def add_path(self, name):
        self.children.add(name)

lines = None
with open("sample") as file:
    lines = [line.strip("\n") for line in file]

all_valves = {}
all_rewards = set()

for line in lines:
        parsed = re.findall(r'[A-Z]{2}|\d+', line)
        name = parsed[0]
        rate = int(parsed[1])

        valve = Valve(name, rate)
        # Treat the openning of a valve as a whole new path that brings
        # to a new state where the exists are the same but the valve is open
        open_valve = Valve(name+"_OPEN", rate)
        for i in range (2, len(parsed)):
            valve.add_path(parsed[i])
            open_valve.add_path(parsed[i])

        if open_valve.rate > 0:
            # all_valves[open_valve.name] = open_valve
            all_rewards.add(open_valve.name)
            # valve.add_path(open_valve.name)

        all_valves[valve.name] = valve
        

def solve():
    # Init frontier
    frontier = StackFrontier()
    start = all_valves["AA"]
    frontier.add(Node(name=start.name, parent=None)) 

    results = []
    while True:
        # If nothing is empty, there is no solutionn
        if frontier.empty():
            return results

        # Fetch new node to explore
        node = frontier.remove()

        # Check if exit conditions were reached
        if node.time <= 0:
            if node.time == 0:
                results.append(node.pressure)
            continue

        if len(all_rewards) == node.explored:
            pressure = node.pressure + node.rate * node.time
            results.append(pressure)
            continue

        if node.time < 15 and node.rate == 0:
            continue

        explored = set()
        for val in node.explored:
            explored.add(val)
        time = node.time
        pressure = node.pressure
        rate = node.rate

        # print("Exploring: " + node.name)

        # can_move = False
        # for child in all_valves[node.name].children:
        #     if child not in explored:
        #         can_move = True

        # # Check if cant move anymore
        # if not can_move:
        #     # print("PATH ENDED ON ROAD:")
        #     reward = 0
        #     while node.parent is not None:
        #         print("-> PATH WAS: "+node.name)
        #         reward += node.rate
        #         node = node.parent
        #     results.append(reward)
        #     continue

        # Mark node as explored
        # if node.name in all_rewards:
        #     explored.add(node.name)
        time -= 1
        pressure += node.rate
        if all_valves[node.name].rate > 0 and node.name+"_OPEN" not in explored:
            explored.add(node.name+"_OPEN")
            time -= 1
            rate += all_valves[node.name].rate #TODO before or after?
        print(f"====== TIME: {time}")
        print(f"====== SIZE: {frontier.size()}")

        
        # Add children to frontier
        for child in all_valves[node.name].children:
            if child not in explored:
                # print("ADDING CHILD :"+child+" WITH PARENT: "+node.name)
                valve = all_valves[child]
                new_node = Node(name=valve.name, parent=node)
                new_node.explored = explored
                new_node.time = time
                new_node.pressure = pressure
                new_node.rate = rate
                frontier.add(new_node)
        # input("")
        if len(results) > 0:
            print(max(results))

results = solve()
print(f"PART_ONE: {max(results)}")