from enum import Enum

lines = None
with open("input.txt") as file:
    lines = [line.strip("\n") for line in file]

class FILE_TYPE (Enum):
    FOLDER = 0
    FILE = 1

class Node():
    def __init__(self, name, type = FILE_TYPE.FOLDER, size = 0):
        self.name = name
        self.type = type
        self.size = int(size)
        self.children = []
        self.parent = None

    def add_child(self, new_node):
        prev_node = self.get_child_by_name(new_node.name)
        if prev_node is not None:
            print('\033[93m' +"cannot add two children with the same name" + '\033[0m')
            return
        new_node.parent = self
        self.children.append(new_node)

    def get_child_by_name(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

    def get_parent(self):
        return self.parent

# FILE SYSTEM
fs = Node("/")
p = fs

def exe_cmd(cmd, arg = None):
    global p
    if cmd == "cd":
        if arg == "/":
            print(f"moving to root")
            p = fs
        elif arg == "..":
            print(f"moving to parent")
            new_folder = p.get_parent()
            if new_folder is None:
                print('\033[91m' +"failed to move to parent" + '\033[0m')
                return
            p = new_folder
        else:
            print(f"moving to {arg}")
            new_folder = p.get_child_by_name(arg)
            if new_folder is None:
                print('\033[91m' + f"failed to move to {arg}" + '\033[0m')
                return
            p = new_folder

    if cmd == "ls":
        print("checking")


for line in lines:
    if line[0] == '$':
        parsed = line.split()
        cmd = parsed[1]
        arg = None if len(parsed) == 2 else parsed[2]
        exe_cmd(cmd, arg)
        continue

    if line[0] == 'd':
        parsed = line.split()
        name = parsed[1]
        new_child = Node(name)
        p.add_child(new_child)
        continue
    
    if line[0].isdigit():
        parsed = line.split()
        size = parsed[0]
        name = parsed[1]
        new_child = Node(name, FILE_TYPE.FILE, size)
        p.add_child(new_child)

    else:
        print('\033[91m' + f"ERROR READING LINE \"{line}\"" + '\033[0m')

folders = []
all_folders = []
def get_folder_size(pointer: Node):
    size = 0
    for child in pointer.children:
        if child.type == FILE_TYPE.FILE:
            size += child.size
        else:
            size += get_folder_size(child)
    
    if size <= 100000:
        folders.append(size)
    all_folders.append(size)
    return size

root_size = get_folder_size(fs)
print(f"\nPART ONE = {sum(folders)}\n")

empty_size = 70000000 - root_size
needed_size = 30000000 - empty_size
to_remove = 70000000
for size in all_folders:
    if size >= needed_size:
        if size < to_remove:
            to_remove = size

print(f"PART TWO = {to_remove}\n")

