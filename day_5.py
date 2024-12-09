from collections import namedtuple
from pathlib import Path
from typing import List, Set
from rich import print


Rule = namedtuple("Rule", "x y")
Update = List[int]


def parse_rules(rules_file: Path):

    rules: List[Rule] = []

    with open(rules_file, mode="r") as file:
        for line in file.readlines():
            line.strip("\n")
            x, y = line.split("|")
            rules.append(Rule(int(x), int(y)))

    return rules


def parse_updates(updates_file: Path):
    updates: List[Update] = []

    with open(updates_file, mode="r") as file:
        for line in file.readlines():
            update_str = line.split(",")
            updates.append([int(x.strip("\n")) for x in update_str])

    return updates


def is_update_valid(update: Update, rules: List[Rule]): ...


if __name__ == "__main__":

    rules = parse_rules("./day_5_input_rules.txt")
    updates = parse_updates("./day_5_input_updates.txt")
