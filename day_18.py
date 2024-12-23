from heapq import heappop
from pathlib import Path
from typing import List, NamedTuple


class Coordinate(NamedTuple):
    row: int
    col: int

    def __add__(self, other: "Coordinate"):
        return Coordinate(self.row + other.row, self.col + other.col)


class State(NamedTuple):
    cost: int
    position: Coordinate


DIRECTIONS = [Coordinate(-1, 0), Coordinate(0, 1), Coordinate(1, 0), Coordinate(0, -1)]

ROW_MAX = 70
COL_MAX = 70
CORRUPTED_BLOCKS = 1024
START = Coordinate(0, 0)
END = Coordinate(70, 70)


def parse_input(file_path: Path) -> List[Coordinate]:
    with open(file_path, mode="r") as file:
        coordinates = []
        for line in file.readlines():
            row, col = map(int, line.strip().split(","))
            coordinates.append(Coordinate(row, col))
        return coordinates


if __name__ == "__main__":

    corrupted_blocks = parse_input(Path("./day_18_input.txt"))

    initial_state = State(cost=0, position=START)

    heap = [initial_state]

    visited = set()

    best = None

    while heap:
        current_state = heappop(heap)

        if current_state.position == END and best == None:
            best = current_state.cost
        if current_state.position in visited:
            continue
        visited.add(current_state.position)

        for dir in DIRECTIONS:
            next_position = current_state.position + dir
            if (
                0 <= next_position.row <= ROW_MAX
                and 0 <= next_position.col <= COL_MAX
                and next_position not in corrupted_blocks[:CORRUPTED_BLOCKS]
            ):
                next_state = State(cost=current_state.cost + 1, position=next_position)
                heap.append(next_state)

    print(best)
