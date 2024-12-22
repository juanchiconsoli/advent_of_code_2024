from collections import defaultdict
from pathlib import Path
from typing import NamedTuple, List, Dict, Tuple
from rich import print
from heapq import heappop, heappush
from rich import print


class Coordinate(NamedTuple):
    row: int
    col: int

    def __add__(self, other: "Coordinate"):
        return Coordinate(self.row + other.row, self.col + other.col)


DIRECTIONS = [Coordinate(-1, 0), Coordinate(0, 1), Coordinate(1, 0), Coordinate(0, -1)]


class State(NamedTuple):
    cost: int
    position: Coordinate
    direction: Coordinate


def parse_grid(file_path: str) -> Dict[str, List[Coordinate]]:
    grid = defaultdict(list)
    with open(file_path, "r") as file:
        for row_idx, line in enumerate(file):
            for col_idx, char in enumerate(line.strip()):
                grid[char].append(Coordinate(row=row_idx, col=col_idx))
    return grid


def get_neighbors(state: State, grid: Dict[str, List[Coordinate]]) -> List[State]:

    neighbors = []

    # Move forward
    new_pos = state.position + state.direction

    if new_pos in grid.get(".", []) or new_pos in grid.get("E", []):
        neighbors.append(State(state.cost + 1, new_pos, state.direction))

    # Rotate clockwise
    new_direction = Coordinate(state.direction.col, -state.direction.row)
    neighbors.append(State(state.cost + 1000, state.position, new_direction))

    # Rotate counterclockwise
    new_direction = Coordinate(-state.direction.col, state.direction.row)
    neighbors.append(State(state.cost + 1000, state.position, new_direction))

    return neighbors


def find_lowest_score(grid: Dict[str, List[Coordinate]]) -> int:
    start = grid["S"][0]
    end = grid["E"][0]
    initial_state = State(cost=0, position=start, direction=Coordinate(0, 1))

    heap = [initial_state]
    visited = set()
    path = {}

    best = None

    while heap:
        current_state = heappop(heap)

        if (current_state.position, current_state.direction) not in path:
            path[(current_state.position, current_state.direction)] = current_state.cost

        if current_state.position == end and best == None:
            best = current_state.cost
        if (current_state.position, current_state.direction) in visited:
            continue
        visited.add((current_state.position, current_state.direction))

        for neighbor in get_neighbors(current_state, grid):
            if (neighbor.position, neighbor.direction) not in visited:
                heappush(heap, neighbor)

    return best, path


def find_optimal_paths_coordinates(
    grid: Dict[str, List[Coordinate]],
    best_score: int,
    path: Dict[Tuple[Coordinate, Coordinate], int],
) -> List[Coordinate]:

    heap: List[Tuple[int, Coordinate, Coordinate]] = []
    visited = set()
    path2 = {}

    for dir in DIRECTIONS:
        heappush(heap, (0, grid["E"][0], dir))

    while heap:
        current_cost, current_pos, current_dir = heappop(heap)

        if (current_pos, current_dir) not in path2:
            path2[(current_pos, current_dir)] = current_cost

        if (current_pos, current_dir) in visited:
            continue
        visited.add((current_pos, current_dir))

        new_dir = Coordinate(-current_dir.row, -current_dir.col)
        new_pos = current_pos + new_dir

        if new_pos in grid.get(".", []) or new_pos in grid.get("S", []):
            heappush(heap, (current_cost + 1, new_pos, current_dir))

        for dir in DIRECTIONS:
            heappush(heap, (current_cost + 1000, current_pos, dir))

    Ok = set()

    for r in grid.get("."):
        for dir in DIRECTIONS:
            if (
                (r, dir) in path
                and (r, dir) in path2
                and path[(r, dir)] + path2[(r, dir)] == best_score
            ):
                Ok.add(r)

    return Ok


# Example usage
if __name__ == "__main__":
    file_path = Path("./day_16_input.txt")
    grid = parse_grid(file_path)

    best_score, path = find_lowest_score(grid)

    optimal_paths = find_optimal_paths_coordinates(grid, best_score, path)

    print(best_score)

    print(
        len(optimal_paths) + 2
    )  # +2 because we need to include the start and end points
