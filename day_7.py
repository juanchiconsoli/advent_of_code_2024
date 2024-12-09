from pathlib import Path
from typing import List
from collections import namedtuple
from rich import print

Equation = namedtuple("Equation", "result operands")


def parse_input(file: Path) -> List[Equation]:

    equations = []

    if not file.exists():
        raise FileNotFoundError(f"file {file} didn't exist")

    with open(file, mode="r") as equation_file:
        for line in equation_file.readlines():
            eq = line.split(":")

            result = int(eq[0])
            operands = _clean_operands(eq[1])

            equations.append(Equation(result, operands))

    return equations


def _clean_operands(operands: str):

    clean_operands: List[int] = []

    operands_split = operands.split(" ")

    for operand in operands_split:
        operand = operand.strip().strip("\n")

        try:
            clean_operands.append(int(operand))
        except ValueError:
            ...

    return clean_operands


def is_valid(eq: Equation):

    if not eq.operands:
        return False

    def evaluate(index: int, current_operand: int) -> bool:

        if index == len(eq.operands):
            return current_operand == eq.result

        next_operand = eq.operands[index]

        # Sum
        if evaluate(index + 1, current_operand + next_operand):
            return True

        # Multiplication
        if evaluate(index + 1, current_operand * next_operand):
            return True

        # Concatenation
        concatenated_value = int(str(current_operand) + str(next_operand))

        if evaluate(index + 1, concatenated_value):
            return True

        # If none of the operations work, return False
        return False

    # Start recursion from the first operand
    return evaluate(1, eq.operands[0])


if __name__ == "__main__":

    valid_results: List[int] = []

    equations = parse_input(Path("./day_7_input.txt"))

    for eq in equations:

        if is_valid(eq):
            valid_results.append(eq.result)

    sum_results = sum(x for x in valid_results)

    print(
        f"Analizamos {len(equations)} ecuaciones de las cuales {len(valid_results)} eran validas."
    )
    print(f"La suma de todos los resultados validos es {sum_results}")
