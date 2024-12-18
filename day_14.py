# robots position and velocity p: (x,y) and v: (vx,vy) in tiles per second (x col, y row)
# grid is 101 wide 103 tall
# robots teleport in edges

from pathlib import Path
import re
from typing import List, NamedTuple
from rich import print


WIDTH = 101
HEIGHT = 103


class Coordinate(NamedTuple):
    row: int
    col: int

    def __add__(self, other: "Velocity"):
        if isinstance(other, Velocity):
            return Coordinate(self.row + other.v_r, self.col + other.v_c)
        else:
            raise ValueError


class Velocity(NamedTuple):
    v_r: int
    v_c: int

    def __mul__(self, other):
        if isinstance(other, int):
            return Velocity(self.v_r * other, self.v_c * other)
        else:
            raise NotImplementedError


class Robot:

    def __init__(self, initial_position: Coordinate, velocity: Velocity):
        self._position = initial_position
        self._velocity = velocity

    def get_position(self, t: int):

        for _ in range(t):

            pos = self._position + self._velocity

            self._position = Coordinate(pos.row % HEIGHT, pos.col % WIDTH)

        return self._position

    def __repr__(self):
        return f"Robot(p={self._position}, v={self._velocity})"


def parse_input(file_path: Path) -> List[Robot]:
    robots = []

    with open(file_path, mode="r") as file:
        for line in file.readlines():
            px, py, vx, vy = [int(x) for x in re.findall("-?\d+", line)]

            robots.append(Robot(Coordinate(py, px), Velocity(vy, vx)))

    return robots


def part_1():

    robots = parse_input(Path("./day_14_input.txt"))

    t = 100

    positions = [r.get_position(t) for r in robots]

    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    for pos in positions:
        if pos.row < HEIGHT // 2 and pos.col < WIDTH // 2:
            q1 += 1
        elif pos.row < HEIGHT // 2 and pos.col > WIDTH // 2:
            q2 += 1
        elif pos.row > HEIGHT // 2 and pos.col < WIDTH // 2:
            q3 += 1
        elif pos.row > HEIGHT // 2 and pos.col > WIDTH // 2:
            q4 += 1

    print(f"q1={q1}, q2={q2}, q3={q3}, q4={q4}")
    print(q1 * q2 * q3 * q4)


def create_empty_grid():

    g = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

    return g


def print_grid(t: int, grid: List[List[str]]):

    with open(Path("./day_14_output.txt"), mode="a+", encoding="utf-8") as file:
        file.write(f"Iteration t={t}\n\n")
        for r in grid:
            file.write("".join(r) + "\n")


def part_2():
    robots = parse_input(Path("./day_14_input.txt"))

    t_max = 10000

    for t in range(7750, 7790):

        grid = create_empty_grid()

        positions = set([r.get_position(t) for r in robots])

        for p in positions:
            grid[p.row][p.col] = "#"

        print_grid(t, grid)


if __name__ == "__main__":
    part_2()
