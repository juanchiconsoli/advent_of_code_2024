from collections import namedtuple
from pathlib import Path
from typing import List
from rich import print


class OutOfGrid(Exception): ...


Coordinate = namedtuple("Coordinate", "x y")

Direction = namedtuple("Direction", "dx dy")


def parse_grid(file_path: Path) -> List[str]:

    grid = []

    with open(file_path, mode="r") as file:
        for line in file.readlines():
            grid.append(line.strip("\n"))

    return grid


class Grid:

    def __init__(self, grid: List[str]) -> None:
        self.coordinates = grid
        self.x_max = len(self.coordinates[0])
        self.y_max = len(self.coordinates)

    def get_coordinate_character(self, coordinate: Coordinate):
        if self.is_coordinate_within_limits(coordinate):
            return self.coordinates[coordinate.y][coordinate.x]
        else:
            raise OutOfGrid("Coordinate is out of grid")

    def is_coordinate_within_limits(self, coordinate: Coordinate):

        if coordinate.x in range(self.x_max) and coordinate.y in range(self.y_max):
            return True
        else:
            return False

    def mark_character(self, coordinate: Coordinate, character: str):

        self.coordinates[coordinate.y] = (
            self.coordinates[coordinate.y][: coordinate.x]
            + character
            + self.coordinates[coordinate.y][coordinate.x + 1 :]
        )


class Guard:

    path_marker = "X"

    def __init__(
        self,
        direction_x: int,
        direction_y: int,
        position_x: int,
        position_y: int,
    ) -> None:
        self.direction = Direction(direction_x, direction_y)
        self.position = Coordinate(position_x, position_y)

    def change_direction(self):

        if self.direction == Direction(0, -1):
            self.direction = Direction(1, 0)
        elif self.direction == Direction(1, 0):
            self.direction = Direction(0, 1)
        elif self.direction == Direction(0, 1):
            self.direction = Direction(-1, 0)
        elif self.direction == Direction(-1, 0):
            self.direction = Direction(0, -1)
        else:
            raise ValueError("Invalid Direction")
        
    def next_step_coordinate(self):
        return Coordinate(
            self.position.x + self.direction.dx, self.position.y + self.direction.dy
        )

    def walk(self):
        self.position = Coordinate(
            self.position.x + self.direction.dx, self.position.y + self.direction.dy
        )

        return self.position


class GridWalker:

    def __init__(self, grid: Grid, guard: Guard) -> None:
        self.grid = grid
        self.guard = guard

    def mark_guard_path(self):

        self.grid.mark_character(self.guard.position, character=Guard.path_marker)

        try:
            while 1:
                next_step_coordinate = self.guard.next_step_coordinate()

                if not grid.is_coordinate_within_limits(next_step_coordinate):
                    self.grid.mark_character(
                        self.guard.position, character=Guard.path_marker
                    )
                    raise OutOfGrid("Guard left the grid")

                next_character = grid.get_coordinate_character(next_step_coordinate)

                if self.is_obstacle(next_character):
                    self.guard.change_direction()

                self.grid.mark_character(
                    self.guard.position, character=Guard.path_marker
                )

                self.guard.walk()

        except OutOfGrid:
            print("Guard is finally out of the grid")

    def is_obstacle(self, character: str):
        return character == "#"

    def count_guard_positions_in_grid(self):

        count = 0

        for x in range(self.grid.x_max):
            for y in range(self.grid.y_max):
                if self.grid.coordinates[x][y] == Guard.path_marker:
                    count += 1

        return count


def get_guard_in_grid(grid: Grid):

    def is_guard(character: str):
        return (
            character == "^" or character == ">" or character == "v" or character == "<"
        )

    def get_guard_direction(guard: str):
        if guard == "^":
            return Direction(0, -1)
        elif guard == ">":
            return Direction(1, 0)
        elif guard == "v":
            return Direction(0, 1)
        elif guard == "<":
            return Direction(-1, 0)
        else:
            raise ValueError("Invalid direction")

    for y in range(grid.y_max):
        for x in range(grid.x_max):
            if is_guard(grid.coordinates[y][x]):
                position = Coordinate(x, y)
                direction = get_guard_direction(grid.coordinates[y][x])

                return Guard(
                    direction_x=direction.dx,
                    direction_y=direction.dy,
                    position_x=position.x,
                    position_y=position.y,
                )


if __name__ == "__main__":
    grid_parsed = parse_grid(Path("day_6_input.txt"))

    grid = Grid(grid_parsed)

    guard = get_guard_in_grid(grid)

    lab_map_walker = GridWalker(grid=grid, guard=guard)

    print(f"Guard Initial Position - {guard.position}")

    print(f"Guard Initial Direction - {guard.direction}")

    lab_map_walker.mark_guard_path()

    guard_positions = lab_map_walker.count_guard_positions_in_grid()

    print(f"The guard passed through {guard_positions} distinct positions in the grid")
