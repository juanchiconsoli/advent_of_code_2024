# Claw machine: two buttons A and B
# A costs 3 tokens
# B costs 1 token
# Each button moves a specific direct in the X, Y axis
# each button would need to be pressed no more than 100 times to win a prize

from pathlib import Path
from typing import List, NamedTuple
from rich import print


class UnsolvableMachine(Exception): ...


class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coordinate"):
        return Coordinate(self.x + other.x, self.y + other.y)


class ClawMachine:
    cost_a = 3
    cost_b = 1

    def __init__(self, a: Coordinate, b: Coordinate, p: Coordinate):
        self.a: Coordinate = a
        self.b: Coordinate = b
        self.p: Coordinate = p
        self.cost = None

    def solve(self):
        """
        Ax.x + Bx.y = Px
        Ay.x + By.y = Py
        """
        determinante = self.a.x * self.b.y - self.a.y * self.b.x
        determinante_x = self.p.x * self.b.y - self.p.y * self.b.x
        determinante_y = self.a.x * self.p.y - self.a.y * self.p.x

        x = determinante_x / determinante
        y = determinante_y / determinante

        if not x.is_integer() or not y.is_integer():
            raise UnsolvableMachine("The machine has no discrete solution")

        self.cost = x * self.cost_a + y * self.cost_b

    def __repr__(self):
        return f"ClawMachine(a={self.a}, b={self.b}, p={self.p}), cost={self.cost}"


def parse_machines(file_path: Path, unit_convertion: bool = False):

    machines: List[ClawMachine] = []

    with open(file_path, mode="r") as file:
        machine_definitions = file.read().strip().split("\n\n")

    for machine in machine_definitions:
        a, b, prize = machine.split("\n")
        aw = a.split()
        ax = int(aw[2].split("+")[1].split(",")[0])
        ay = int(aw[3].split("+")[1].split(",")[0])
        bw = b.split()
        bx = int(bw[2].split("+")[1].split(",")[0])
        by = int(bw[3].split("+")[1].split(",")[0])
        pw = prize.split()
        px = int(pw[1].split("=")[1].split(",")[0])
        py = int(pw[2].split("=")[1])

        if unit_convertion:
            px = px + 10000000000000
            py = py + 10000000000000

        machines.append(
            ClawMachine(
                a=Coordinate(ax, ay), b=Coordinate(bx, by), p=Coordinate(px, py)
            )
        )

    return machines


if __name__ == "__main__":
    machines = parse_machines(Path("./day_13_input.txt"), unit_convertion=True)

    cost = 0

    for machine in machines:
        try:
            machine.solve()
            if machine.cost is not None:
                cost += machine.cost
        except UnsolvableMachine:
            continue

    print(machines[:4])
    print(cost)
