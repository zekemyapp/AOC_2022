from tqdm import tqdm
PART_TWO = False
ROUNDS = 10000 if PART_TWO else 20

class Monkey():
    def __init__(self, items, operation, divisor, truer, falser):
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.truer = truer
        self.falser = falser
        self.n_inspections = 0

    def item_size(self):
        return len(self.items)

    def add_item(self, item):
        self.items.append(item)

    def get_item(self):
        return self.items.pop(0)

    def inspect_one(self, item):
        self.n_inspections += 1
        new_item = self.operation(item)
        return self.chill(new_item)

    def inspect_two(self, item, reducer):
        self.n_inspections += 1
        new_item = self.operation(item)
        new_item = new_item % reducer
        new_monkey = self.truer if new_item % self.divisor == 0 else self.falser
        return new_item, new_monkey

    def chill(self, item):
        return item // 3

    def test(self, item):
        if item % self.divisor == 0:
            return self.truer
        else:
            return self.falser

# Sample
# monkeys = [
#     Monkey([79, 98], lambda a : a * 19, divisor=23, truer=2, falser=3),
#     Monkey([54, 65, 75, 74], lambda a : a + 6, divisor=19, truer=2, falser=0),
#     Monkey([79, 60, 97], lambda a : a * a, divisor=13, truer=1, falser=3),
#     Monkey([74], lambda a : a + 3, divisor=17, truer=0, falser=1)
# ]

# Input
monkeys = [
    Monkey([83, 62, 93], lambda a : a * 17, divisor=2, truer=1, falser=6),
    Monkey([90, 55], lambda a : a + 1, divisor=17, truer=6, falser=3),
    Monkey([91, 78, 80, 97, 79, 88], lambda a : a + 3, divisor=19, truer=7, falser=5),
    Monkey([64, 80, 83, 89, 59], lambda a : a + 5, divisor=3, truer=7, falser=2),
    Monkey([98, 92, 99, 51], lambda a : a * a, divisor=5, truer=0, falser=1),
    Monkey([68, 57, 95, 85, 98, 75, 98, 75], lambda a : a + 2, divisor=13, truer=4, falser=0),
    Monkey([74], lambda a : a + 4, divisor=7, truer=3, falser=2),
    Monkey([68, 64, 60, 68, 87, 80, 82], lambda a : a * 19, divisor=11, truer=4, falser=5),
]

n_monkeys  = len(monkeys)
reducer = 1
for monkey in monkeys:
    reducer *= monkey.divisor

# Rounds
for round in tqdm(range(ROUNDS)):
    # Turns
    for i in tqdm(range(n_monkeys), leave=False):
        monkey = monkeys[i]
        # Items held
        while monkey.item_size() != 0:
            item = monkey.get_item()
            if PART_TWO:
                new_item, new_monkey = monkey.inspect_two(item, reducer)
            else:
                new_item = monkey.inspect_one(item)
                new_monkey = monkey.test(new_item)
            monkeys[new_monkey].add_item(new_item)

results = [monkeys[i].n_inspections for i in range(n_monkeys)]
results.sort(reverse=True)
print(f"PART ONE = {results[0] * results[1]}")