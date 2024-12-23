from collections import defaultdict
from typing import Set


edges = [line.strip().split("-") for line in open("./day_23_input.txt")]
conns = defaultdict(set)

for x, y in edges:
    conns[x].add(y)
    conns[y].add(x)

sets: Set[str] = set()

for x in conns:
    for y in conns[x]:
        for z in conns[y]:
            if x != z and x in conns[z]:
                sets.add(tuple(sorted([x, y, z])))

print(len([s for s in sets if any(cn.startswith("t") for cn in s)]))
