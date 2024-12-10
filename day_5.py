from collections import namedtuple
from pathlib import Path
from typing import List
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


if __name__ == "__main__":
    rules = parse_rules(Path("./day_5_input_rules.txt"))
    updates = parse_updates(Path("./day_5_input_updates.txt"))

    valid_updates: List[int] = []

    for update in updates:

        if is_update_valid(rules, update):
            middleIndex = findMiddle(update)
            valid_updates.append(update[middleIndex])

    sum_of_middles = sum(x for x in valid_updates)

    print(
        f"There were {len(valid_updates)} valid updates in a list of {len(updates)} updates. The sum of the middle pages for the valid updates is {sum_of_middles}"
    )
