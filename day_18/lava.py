import math
from tqdm import tqdm

def distance_sqrt(cube_a, cube_b):
  distance = ((cube_b[2]-cube_a[2])**2 +
               (cube_b[1]-cube_a[1])**2 + 
               (cube_b[0]-cube_a[0])**2)
  return distance

with open("input") as file:
    lines = [line.strip("\n") for line in file]

cubes = []
for line in lines:
        _cube = [int(c) for c in line.split(',')]
        cubes.append(tuple(_cube))

cubes_touching = set()
for cube_a in tqdm(cubes):
        for cube_b in tqdm(cubes, leave=False):
                if (cube_a, cube_b) in cubes_touching or (cube_b, cube_a) in cubes_touching:
                        continue
                distance = distance_sqrt(cube_a, cube_b)

                if distance == 0:
                        # same cube
                        continue

                if distance == 1:
                        # cubes touching
                        cubes_touching.add((cube_a, cube_b))
                        cubes_touching.add((cube_b, cube_a))

def get_adj(cube):
        right = (cube[0]+1, cube[1], cube[2])
        left = (cube[0]-1, cube[1], cube[2])
        up = (cube[0], cube[1]+1, cube[2])
        down = (cube[0], cube[1]-1, cube[2])
        out = (cube[0], cube[1], cube[2]+1)
        inside = (cube[0], cube[1], cube[2]-1)

        return [right, left, up, down, out, inside]

def is_enclosed(space, known_side, deepness=0):
        if deepness == 20:
                return False

        adj = get_adj(space)
        enclosed = True

        # For every adjecent cube check if there is a cube.
        # If there isnt, check if the space is enclosed
        for cube in adj:
                # Cube is the known side so no need to explore it
                if cube == known_side:
                        continue

                # Cube is a cube so enclisivity is not yet disproven
                if cube in cubes:
                        continue

                # No cube found in the given space
                # Check if the space is also enclosed
                enclosed = is_enclosed(cube, space, deepness+1)
                if not enclosed:
                        # No need to continue
                        return False
        return enclosed


# STARTS HERE
spaces = set()
for cube in tqdm(cubes):
        adj = get_adj(cube)
        for space in adj:
                if space not in cubes:
                        spaces.add(space)

all_enclosed = set()
for space in tqdm(spaces):
        if is_enclosed(space, None):
                all_enclosed.add(space)
                

spaces_touching = set()
for space_a in tqdm(all_enclosed):
        for space_b in tqdm(all_enclosed, leave=False):
                if (space_a, space_b) in cubes_touching or (space_b, space_a) in spaces_touching:
                        continue
                distance = distance_sqrt(space_a, space_b)

                if distance == 0:
                        # same space
                        continue

                if distance == 1:
                        # spaces touching
                        spaces_touching.add((space_a, space_b))
                        spaces_touching.add((space_b, space_a))


sides = (len(cubes) * 6) - len(cubes_touching)
print(sides)
sides = (len(cubes) * 6) - len(cubes_touching) - (len(all_enclosed) * 6) + len(spaces_touching)
print(sides)

# 4168
# 3683
# 3599 TO HIGH
# 3521 NO INFO


