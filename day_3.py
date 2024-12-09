from pathlib import Path
import re
from typing import List
from rich import print


def parse_input(file: Path) -> str:

    if not file.exists():
        raise FileNotFoundError(f"file {file} didn't exist")

    with open(file, mode="r") as memory_dump:
        return memory_dump.read()


def sum_according_to_instructions(instructions: List[str | int]) -> int:

    result = 0
    enable = True

    for instruction in instructions:
        if instruction == "do()":
            enable = True
        elif instruction == "don't()":
            enable = False
        else:
            if enable and isinstance(instruction, int):
                result += instruction

    return result


if __name__ == "__main__":

    memory_dump = parse_input(Path("day_3_input.txt"))

    mul_pattern = r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)"

    matches = re.finditer(mul_pattern, memory_dump)

    instructions: List[str | int] = []

    for m in matches:
        if m.group(1) and m.group(2):  # Check if it's a "mul(X, Y)"
            instructions.append(int(m.group(1)) * int(m.group(2)))
        else:
            instructions.append(m.group(0))

    result = sum_according_to_instructions(instructions)

    print(
        f"Found {len(instructions)} instructions in the memory dump. The addition of all resutls is {result}"
    )
