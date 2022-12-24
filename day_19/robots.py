import re
from tqdm import tqdm

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
        self.bp = bp

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0

        self.queued_ore_robots = 0
        self.queued_clay_robots = 0
        self.queued_obsidian_robots = 0
        self.queued_geode_robots = 0

    def gather(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes += self.geode_robots

    def build_ore_robot(self):
        if (self.ore >= self.bp.ore_robot.ore_cost and
            self.clay >= self.bp.ore_robot.clay_cost and
            self.obsidian >= self.bp.ore_robot.obsidian_cost):
            
            self.queued_ore_robots += 1
            self.ore -= self.bp.ore_robot.ore_cost
            self.clay -= self.bp.ore_robot.clay_cost
            self.obsidian -= self.bp.ore_robot.obsidian_cost

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
    
    def finish_robots(self):
        self.ore_robots += self.queued_ore_robots
        self.clay_robots += self.queued_clay_robots
        self.obsidian_robots += self.queued_obsidian_robots
        self.geode_robots += self.queued_geode_robots

        self.queued_ore_robots = 0
        self.queued_clay_robots = 0
        self.queued_obsidian_robots = 0
        self.queued_geode_robots = 0

lines = None
with open("sample") as file:
    lines = [line.strip("\n") for line in file]

all_blueprints = []
for line in lines:
    parsed = re.findall(r'\d+', line)
    all_blueprints.append(Blueprint(parsed))

all_results = {}
for bp in tqdm(all_blueprints):

    exe = Execution(bp)

    first_geode = False
    first_obsidian = False
    first_clay = False
    for step in tqdm(range(24), leave=False):
        ################################
        # Blueprint Logic
        ################################

        # Build Geode Robots
        if exe.build_geode_robot() and not first_geode:
            first_geode = True

        # Build Obsidian Robots
        if exe.obsidian < bp.geode_robot.obsidian_cost and not first_geode:
            if exe.build_obsidian_robot() and not first_obsidian:
                first_obsidian = True

        # Build Clay Robots
        expensier = max(bp.obsidian_robot.clay_cost, bp.obsidian_robot.ore_cost)
        if expensier == bp.obsidian_robot.clay_cost:
            next_step_resource = exe.clay+(exe.clay_robots+exe.queued_clay_robots)*2
        else:
            next_step_resource = exe.ore+(exe.ore_robots+exe.queued_ore_robots)*2
        if next_step_resource < expensier and not first_obsidian:
            if exe.build_clay_robot() and not first_clay:
                first_clay = True

        # Build Ore Robots
        if exe.ore < bp.clay_robot.ore_cost:
            if bp.ore_robot.ore_cost < bp.clay_robot.ore_cost:
                exe.build_ore_robot()
        else:
            if not first_clay:
                if exe.build_clay_robot() and not first_clay:
                    first_clay = True

        # Gather resources
        exe.gather()

        # Finish robots
        exe.finish_robots()

        print(f"\State [{step+1}]: [{exe.ore_robots}, {exe.clay_robots}, {exe.obsidian_robots}, {exe.geode_robots}]")
        input("")
        ##############
        # End
        ##############

    print(f"\nFinal state [{bp.id}]: [{exe.ore_robots}, {exe.clay_robots}, {exe.obsidian_robots}, {exe.geode_robots}]")
    all_results[bp.id] = exe.geodes


# Count results
total = 0
for result in all_results:
    print(f"Blueprint[{result}] produced {all_results[result]} geodes")
    total += result * all_results[result]
print(f"PART_ONE: {total}")