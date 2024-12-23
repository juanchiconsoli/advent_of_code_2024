from collections import defaultdict
from typing import Set


edges = [line.strip().split("-") for line in open("./day_23_input.txt")]
conns = defaultdict(set)

for x, y in edges:
    conns[x].add(y)
    conns[y].add(x)

sets: Set[str] = set()

# for x in conns:
#     for y in conns[x]:
#         for z in conns[y]:
#             if x != z and x in conns[z]:
#                 sets.add(tuple(sorted([x, y, z])))

# print(len([s for s in sets if any(cn.startswith("t") for cn in s)]))


def search(node, req):
    key = tuple(sorted(req))
    if key in sets:
        return
    sets.add(key)
    for neighbor in conns[node]:
        if neighbor in req:
            continue
        if not all(neighbor in conns[query] for query in req):
            continue
        search(neighbor, {*req, neighbor})


for x in conns:
    search(x, {x})

print(",".join(sorted(max(sets, key=len))))
