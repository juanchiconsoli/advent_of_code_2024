from collections import defaultdict, deque, namedtuple
from pathlib import Path
from typing import Dict, List
from rich import print

Rule = namedtuple("Rule", "before after")
Update = List[int]


def parse_rules(rules_file: Path):
    rules: List[Rule] = []
    with open(rules_file, mode="r") as file:
        for line in file.readlines():
            line.strip("\n")
            before, after = line.split("|")
            rules.append(Rule(int(before), int(after)))
    return rules


def parse_updates(updates_file: Path):
    updates: List[Update] = []
    with open(updates_file, mode="r") as file:
        for line in file.readlines():
            update_str = line.split(",")
            updates.append([int(x.strip("\n")) for x in update_str])
    return updates


def is_update_valid(rules: List[Rule], update: List[int]):

    for i in range(len(update)):
        for j in range(len(update)):

            current_page = update[i]

            if i < j:
                next_page = update[j]
                if any(
                    r.before == next_page and r.after == current_page for r in rules
                ):
                    return False
            elif i == j:
                continue
            else:
                current_page = update[i]
                previous_page = update[j]

                if any(
                    r.before == current_page and r.after == previous_page for r in rules
                ):
                    return False

    return True


def findMiddle(input_list: List):
    middle = float(len(input_list)) / 2
    if middle % 2 != 0:
        return int(middle - 0.5)
    else:
        return int(middle)


def order_wrong_update(rules: List[Rule], update: List[int]):

    rules_that_apply = [r for r in rules if r.before in update and r.after in update]

    # Step 1: Build the graph and in-degrees
    graph = defaultdict(list)
    in_degree: Dict[int, int] = defaultdict(int)
    nodes = set()

    for before, after in rules_that_apply:
        graph[before].append(after)
        in_degree[after] += 1
        nodes.update([before, after])

    # Ensure all nodes are in the in-degree dictionary
    for node in nodes:
        in_degree[node] += 0

    # Step 2: Perform Topological Sort using Kahn's Algorithm
    queue = deque([node for node in nodes if in_degree[node] == 0])
    sorted_order = []

    while queue:
        current = queue.popleft()
        sorted_order.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_order) != len(nodes):
        raise ValueError("The graph has a cycle! Absolute ordering is not possible.")

    return sorted_order


if __name__ == "__main__":
    rules = parse_rules(Path("./day_5_input_rules.txt"))
    updates = parse_updates(Path("./day_5_input_updates.txt"))

    valid_updates: List[int] = []
    wrong_updates: List[List[int]] = []

    for update in updates:

        if is_update_valid(rules, update):
            middleIndex = findMiddle(update)
            valid_updates.append(update[middleIndex])
        else:
            wrong_updates.append(update)

    sum_of_middles = sum(x for x in valid_updates)

    print(
        f"There were {len(valid_updates)} valid updates in a list of {len(updates)} updates. The sum of the middle pages for the valid updates is {sum_of_middles}"
    )
    print(f"There were {len(wrong_updates)} wrong updates")

    print("Ordering wrong updates using graphs...")

    wrong_updates_ordered = []

    for wrong_update in wrong_updates:
        ordered_update = order_wrong_update(rules, wrong_update)
        wrong_updates_ordered.append(ordered_update[findMiddle(ordered_update)])

    print(
        f"Sum of middles for wrong updates ordered is now {sum(x for x in wrong_updates_ordered)}"
    )
