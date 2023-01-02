from tqdm import tqdm
with open("input") as file:
    lines = [line.strip("\n").replace(":", "") for line in file]

all_monkeys = {}

class Monkey():
    def __init__(self, val=None, op=None, m1=None, m2=None):
        self.val = val
        self.op = op
        self.m1 = m1
        self.m2 = m2

    def has_value(self):
        return self.val is not None

    def get_value(self):
        if self.has_value():
            return self.val
        return self.do_operation()

    def do_operation(self):
        monkey1 = all_monkeys[self.m1]
        monkey2 = all_monkeys[self.m2]
        m1 = monkey1.get_value()
        m2 = monkey2.get_value()

        if self.op == "+":
            return m1 + m2
        
        if self.op == "-":
            return m1 - m2

        if self.op == "*":
            return m1 * m2

        if self.op == "/":
            return m1 / m2

        if self.op == "==" or self.op == "=":
            r = m1 == m2
            return r

    def get_equation(self):
        if self.has_value():
            return str(self.val)
        return self.get_str_operation()

    def get_str_operation(self):
        has_x = False
        if self.m1 == "humn":
            monkey1 = "x"
        else:
            monkey1 = all_monkeys[self.m1].get_equation()

        if self.m2 == "humn":
            monkey2 = "x"
        else:
            monkey2 = all_monkeys[self.m2].get_equation()

        if "x" in monkey1 or "x" in monkey2:
            has_x = True

        if has_x:
            return "("+monkey1+self.op+monkey2+")"
        else:
            return str(eval(monkey1+self.op+monkey2))

for line in lines:
    l = line.split(" ")
    if len(l) == 2:
        name = l[0]
        value = int(l[1])
        all_monkeys[name] = Monkey(val=value)

    else:
        name = l[0]
        m1 = l[1]
        op = l[2]
        m2 = l[3]
        all_monkeys[name] = Monkey(op=op, m1=m1, m2=m2)

print(f"PART_ONE = {all_monkeys['root'].get_value()}")

# PART_TWO
all_monkeys['root'].val = None
all_monkeys['root'].op = "="
equation = all_monkeys['root'].get_equation()
print("PART_TWO: "+equation)