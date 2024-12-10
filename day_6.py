from collections import namedtuple
from pathlib import Path
from typing import Dict, List, Set, Tuple
from rich import print
from copy import deepcopy


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

    def get_state(self) -> Dict[str, Tuple]:

        return {"position": self.position, "direction": self.direction}

    def print_state(self):
        print("Guard State")
        print(self.position)
        print(self.direction)


def sum_vectors(coordinate: Coordinate, direction: Direction):

    if len(coordinate) != len(direction):
        raise ValueError

    return Coordinate(coordinate.x + direction.dx, coordinate.y + direction.dy)


class GridWalker:

    def __init__(self, grid: Grid, guard: Guard) -> None:
        self.grid = grid
        self.guard = guard

        self.inital_position = guard.position
        self.inital_direction = guard.direction

    def get_guard_path(self):

        visited_states: Set[Coordinate] = set()

        visited_states.add((self.guard.position, self.guard.direction))

        next_step_coordinate = self.guard.next_step_coordinate()

        if not grid.is_coordinate_within_limits(next_step_coordinate):
            self.reset_guard()

            return visited_states

        if self.is_obstacle(grid.get_coordinate_character(next_step_coordinate)):
            self.guard.change_direction()

        self.guard.walk()

        while (self.guard.position, self.guard.direction) not in visited_states:
            next_step_coordinate = self.guard.next_step_coordinate()

            if not grid.is_coordinate_within_limits(next_step_coordinate):
                visited_states.add((self.guard.position, self.guard.direction))
                self.reset_guard()

                return visited_states

            if self.is_obstacle(grid.get_coordinate_character(next_step_coordinate)):
                self.guard.change_direction()

            visited_states.add((self.guard.position, self.guard.direction))

            self.guard.walk()

        self.reset_guard()

        return visited_states

    def is_obstacle(self, character: str):
        return character == "#"

    def reset_guard(self):
        self.guard.position = self.inital_position
        self.guard.direction = self.inital_direction

    def find_loop_positions(self):

        possible_positions = set()
        directions = [
            Direction(-1, 0),
            Direction(0, 1),
            Direction(1, 0),
            Direction(0, -1),
        ]

        visited_states = self.get_guard_path()

        visited_coordinates = {x[0] for x in visited_states}

        for coordinate in visited_coordinates:
            for direction in directions:
                potential_obstacle_coordinate: Coordinate = sum_vectors(
                    coordinate, direction
                )

                if (
                    self.grid.is_coordinate_within_limits(potential_obstacle_coordinate)
                    and self.grid.get_coordinate_character(
                        potential_obstacle_coordinate
                    )
                    == "."
                ):
                    temp_grid = Grid(self.grid.coordinates)
                    temp_grid.mark_character(
                        potential_obstacle_coordinate, character="#"
                    )

                    grid_walker = GridWalker(grid=temp_grid, guard=self.guard)

                    new_visited_coordinates = grid_walker.get_guard_path()

                    if len(new_visited_coordinates) < len(
                        visited_coordinates
                    ):  # Loop detected
                        possible_positions.add(potential_obstacle_coordinate)

        return possible_positions


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

    visited_states = list(lab_map_walker.get_guard_path())

    positions = list({x[0] for x in visited_states})

    guard_positions = len(positions)

    print(f"The guard passed through {guard_positions} distinct positions in the grid")

    possible_loop_positions = lab_map_walker.find_loop_positions()

    print(f"{len(possible_loop_positions)}")
