import re
from tqdm import tqdm

PART_TWO = True

if PART_TWO:
    REF_TIME = 32
else:
    REF_TIME = 24

class Node():
    def __init__(self, execution, parent):
        self.execution = execution
        self.parent = parent

# Breadth First Search
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, execution):
        for node in self.frontier:
            if (
                node.execution.ore == execution.ore
                and node.execution.clay == execution.clay
                and node.execution.obsidian == execution.obsidian
                and node.execution.geodes == execution.geodes
                and node.execution.ore_robots == execution.ore_robots
                and node.execution.clay_robots == execution.clay_robots
                and node.execution.obsidian_robots == execution.obsidian_robots
                and node.execution.geode_robots == execution.geode_robots
            ):
                return True
        return False

    def empty(self):
        return len(self.frontier) == 0

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

class RobotDescription():
    def __init__(self, ore_cost, clay_cost, obsidian_cost):
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost = obsidian_cost

class Blueprint():
    def __init__(self, parsed):
        self.id = int(parsed[0])
        self.ore_robot = RobotDescription(int(parsed[1]), 0, 0)
        self.clay_robot = RobotDescription(int(parsed[2]), 0, 0)
        self.obsidian_robot = RobotDescription(int(parsed[3]), int(parsed[4]), 0)
        self.geode_robot = RobotDescription(int(parsed[5]), 0, int(parsed[6]))

class Execution():
    def __init__(self, bp):
        # Blueprint
        self.bp = bp
        self.time = 0

        # Inventory
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

        # Robots
        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0

        # Robots being built
        self.queued_ore_robots = 0
        self.queued_clay_robots = 0
        self.queued_obsidian_robots = 0
        self.queued_geode_robots = 0

    def cpy_execution(self, execution):
        self.time = execution.time

        # Inventory
        self.ore = execution.ore
        self.clay = execution.clay
        self.obsidian = execution.obsidian
        self.geodes = execution.geodes

        # Robots
        self.ore_robots = execution.ore_robots
        self.clay_robots = execution.clay_robots
        self.obsidian_robots = execution.obsidian_robots
        self.geode_robots = execution.geode_robots

    def gather(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes += self.geode_robots

    # Start building an ore robot
    def build_ore_robot(self):
        if (self.ore >= self.bp.ore_robot.ore_cost and
            self.clay >= self.bp.ore_robot.clay_cost and
            self.obsidian >= self.bp.ore_robot.obsidian_cost):
            
            self.queued_ore_robots += 1
            self.ore -= self.bp.ore_robot.ore_cost
            self.clay -= self.bp.ore_robot.clay_cost
            self.obsidian -= self.bp.ore_robot.obsidian_cost
            return True
        return False

    # Start building a clay robot
    def build_clay_robot(self):
        if (self.ore >= self.bp.clay_robot.ore_cost and
            self.clay >= self.bp.clay_robot.clay_cost and
            self.obsidian >= self.bp.clay_robot.obsidian_cost):

            self.queued_clay_robots += 1
            self.ore -= self.bp.clay_robot.ore_cost
            self.clay -= self.bp.clay_robot.clay_cost
            self.obsidian -= self.bp.clay_robot.obsidian_cost
            return True
        return False

    # Start building an obsidian robot
    def build_obsidian_robot(self):
        if (self.ore >= self.bp.obsidian_robot.ore_cost and
            self.clay >= self.bp.obsidian_robot.clay_cost and
            self.obsidian >= self.bp.obsidian_robot.obsidian_cost):

            self.queued_obsidian_robots += 1
            self.ore -= self.bp.obsidian_robot.ore_cost
            self.clay -= self.bp.obsidian_robot.clay_cost
            self.obsidian -= self.bp.obsidian_robot.obsidian_cost
            return True
        return False

    # Start building a geode robot
    def build_geode_robot(self):
        if (self.ore >= self.bp.geode_robot.ore_cost and
            self.clay >= self.bp.geode_robot.clay_cost and
            self.obsidian >= self.bp.geode_robot.obsidian_cost):

            self.queued_geode_robots += 1
            self.ore -= self.bp.geode_robot.ore_cost
            self.clay -= self.bp.geode_robot.clay_cost
            self.obsidian -= self.bp.geode_robot.obsidian_cost
            return True
        return False

    # Finish all queued robots
    def finish_robots(self):
        self.ore_robots += self.queued_ore_robots
        self.clay_robots += self.queued_clay_robots
        self.obsidian_robots += self.queued_obsidian_robots
        self.geode_robots += self.queued_geode_robots

        self.queued_ore_robots = 0
        self.queued_clay_robots = 0
        self.queued_obsidian_robots = 0
        self.queued_geode_robots = 0

# Read input
lines = None
with open("sample") as file:
    lines = [line.strip("\n") for line in file]

# Parse blueprints
all_blueprints = []
for line in lines:
    parsed = re.findall(r'\d+', line)
    all_blueprints.append(Blueprint(parsed))

# Calculate quality level for each blueprint
all_results = {}
for bp in tqdm(all_blueprints):

    exe = Execution(bp)

    # Init frontier
    frontier = StackFrontier()
    frontier.add(Node(execution=exe, parent=None))

    while True:
        # If nothing is empty, there is no solutionn
        if frontier.empty():
            print("NO SOLUTION FOUND")
            break

        # Fetch new node to explore
        node = frontier.remove()
        exe = node.execution

        # Check if goal was reached
        if exe.time == REF_TIME:
            if bp.id not in all_results or all_results[bp.id] < exe.geodes:
                print(f"\nNew max state [{bp.id}]: [{exe.ore_robots}, {exe.clay_robots}, {exe.obsidian_robots}, {exe.geode_robots}] -> {exe.geodes}")
                all_results[bp.id] = exe.geodes
            continue


        if not PART_TWO:
            if (
                exe.time >= 18
                and bp.id in all_results
                and (exe.geodes + ((exe.geode_robots + 2) * (25 - exe.time)) <= all_results[bp.id])
            ):
                continue

            if (
                exe.time >= 22
                and bp.id in all_results
                and (exe.geodes + ((exe.geode_robots + 1) * (25 - exe.time)) <= all_results[bp.id])
            ):
                continue
        else:
            if (
                exe.geode_robots > 0
                and bp.id in all_results
            ):
                left_time = (REF_TIME + 1 - exe.time)
                robots =  exe.geode_robots
                geodes = exe.geodes
                for i in range(left_time):
                    geodes += robots
                    robots += 1
                if geodes <= all_results[bp.id]:
                    continue

        if (
            exe.ore_robots > bp.geode_robot.ore_cost
            and exe.ore_robots > bp.obsidian_robot.ore_cost
            and exe.ore_robots > bp.clay_robot.ore_cost
            and exe.ore_robots > bp.ore_robot.ore_cost
        ):
            continue

        if (exe.clay_robots // 2 + 1) > bp.obsidian_robot.clay_cost:
            continue

        if (exe.obsidian_robots // 2 + 1) > bp.geode_robot.obsidian_cost:
            continue

        # Add neighbors to frontier

        ################################
        # Blueprint Logic
        ################################
        exe.time += 1
        new_exe = Execution(exe.bp)
        new_exe.cpy_execution(exe)

        # Build Geode Robots
        if new_exe.build_geode_robot():
            # Gather resources
            new_exe.gather()
            # Finish robots
            new_exe.finish_robots()
            # Add to frontier
            if not frontier.contains_state(new_exe):
                child = Node(execution=new_exe, parent=node)
                frontier.add(child)
            continue
        
        # Could not build geode check obsidian and create a state
        # where you build and one where you do not build
        if (new_exe.ore >= new_exe.bp.obsidian_robot.ore_cost and
            new_exe.clay >= new_exe.bp.obsidian_robot.clay_cost):

            # Insert case where you build
            new_exe.build_obsidian_robot()
            # Gather resources
            new_exe.gather()
            # Finish robots
            new_exe.finish_robots()
            # Add to frontier
            if not frontier.contains_state(new_exe):
                child = Node(execution=new_exe, parent=node)
                frontier.add(child)

            # Continue with case where you do not buy
            new_exe = Execution(exe.bp)
            new_exe.cpy_execution(exe)

        # Build Clay Robots or Not
        if (new_exe.ore >= new_exe.bp.clay_robot.ore_cost):
            # Insert case where you build
            new_exe.build_clay_robot()
            # Gather resources
            new_exe.gather()
            # Finish robots
            new_exe.finish_robots()
            # Add to frontier
            if not frontier.contains_state(new_exe):
                child = Node(execution=new_exe, parent=node)
                frontier.add(child)

            # Continue with case where you do not buy
            new_exe = Execution(exe.bp)
            new_exe.cpy_execution(exe)


        # Build Ore Robots or not
        if (new_exe.ore >= new_exe.bp.ore_robot.ore_cost):
            # Insert case where you build
            new_exe.build_ore_robot()
            # Gather resources
            new_exe.gather()
            # Finish robots
            new_exe.finish_robots()
            # Add to frontier
            if not frontier.contains_state(new_exe):
                child = Node(execution=new_exe, parent=node)
                frontier.add(child)
            continue

        # Case where no robot is built
        new_exe.gather()
        new_exe.finish_robots()
        if not frontier.contains_state(new_exe):
            child = Node(execution=new_exe, parent=node)
            frontier.add(child)        

        ##############
        # End
        ##############


# Count results
total = 0
prod = 1
for result in all_results:
    print(f"Blueprint[{result}] produced {all_results[result]} geodes")
    total += result * all_results[result]
    prod *= result
print(f"PART_ONE: {total}")
print(f"PART_TWO: {prod}")