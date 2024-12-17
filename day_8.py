## https://adventofcode.com/2024/day/8

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, NamedTuple, Set
from rich import print
from itertools import combinations


class OutOfGrid(Exception): ...


class Coordinate(NamedTuple):
    x: int
    y: int


@dataclass
class Antenna:
    frequency: str
    position: Coordinate

    def __hash__(self):
        return hash(self.frequency)


@dataclass
class Antinode:
    frequency: str
    position: Coordinate

    def __hash__(self):
        return hash(f"{self.frequency}_{self.position.x}_{self.position.y}")


@dataclass
class Space:
    position: Coordinate


class Grid:

    def __init__(self, grid: List[str]) -> None:
        self.coordinates = grid
        self.x_max = len(self.coordinates[0])
        self.y_max = len(self.coordinates)

        self._antennas: List[Antenna] = []

        for y in range(self.y_max):
            for x in range(self.x_max):
                element = self.get_element_in_coordinate(Coordinate(x, y))
                if isinstance(element, Antenna):
                    self._antennas.append(element)

    def get_element_in_coordinate(self, coordinate: Coordinate):
        character = self._get_coordinate_character(coordinate)

        if character == ".":
            return Space(coordinate)
        else:
            return Antenna(frequency=character, position=coordinate)

    def _get_coordinate_character(self, coordinate: Coordinate):
        if self.is_coordinate_within_limits(coordinate):
            return self.coordinates[coordinate.y][coordinate.x]
        else:
            raise OutOfGrid("Coordinate is out of grid")

    def is_coordinate_within_limits(self, coordinate: Coordinate):

        if coordinate.x in range(self.x_max) and coordinate.y in range(self.y_max):
            return True
        else:
            return False

    def get_antennas(self):
        return self._antennas

    def get_antennas_by_frequency(self):
        antennas_by_frequency: Dict[str, Set[Antenna]] = defaultdict(set)

        for antenna in self._antennas:
            antennas_by_frequency[antenna.frequency].add(antenna)

        return antennas_by_frequency

    def get_antinodes_for_antennas(
        self, antenna_1: Antenna, antenna_2: Antenna
    ) -> Set[Antinode]:

        antinodes: Set[Antinode] = set()

        if antenna_1.frequency != antenna_2.frequency:
            return antinodes

        distance_x = antenna_2.position.x - antenna_1.position.x
        distance_y = antenna_2.position.y - antenna_1.position.y

        antinode_1_x = antenna_1.position.x - distance_x
        antinode_1_y = antenna_1.position.y - distance_y

        antinode_1 = Antinode(
            frequency=antenna_1.frequency,
            position=Coordinate(antinode_1_x, antinode_1_y),
        )

        if self.is_coordinate_within_limits(antinode_1.position):
            antinodes.add(antinode_1)

        antinode_2_x = antenna_2.position.x + distance_x
        antinode_2_y = antenna_2.position.y + distance_y

        antinode_2 = Antinode(
            frequency=antenna_2.frequency,
            position=Coordinate(antinode_2_x, antinode_2_y),
        )

        if self.is_coordinate_within_limits(antinode_2.position):
            antinodes.add(antinode_2)

        return antinodes

    def get_antinodes_for_antennas_resonance(
        self, antenna_1: Antenna, antenna_2: Antenna
    ) -> Set[Antinode]:

        antinodes: Set[Antinode] = set()

        if antenna_1.frequency != antenna_2.frequency:
            return antinodes

        distance_x = antenna_2.position.x - antenna_1.position.x
        distance_y = antenna_2.position.y - antenna_1.position.y

        antinode_1_x = antenna_1.position.x
        antinode_1_y = antenna_1.position.y

        while self.is_coordinate_within_limits(Coordinate(antinode_1_x, antinode_1_y)):
            antinodes.add(
                Antinode(
                    frequency=antenna_1.frequency,
                    position=Coordinate(antinode_1_x, antinode_1_y),
                )
            )

            antinode_1_x -= distance_x
            antinode_1_y -= distance_y

        antinode_2_x = antenna_2.position.x
        antinode_2_y = antenna_2.position.y

        while self.is_coordinate_within_limits(Coordinate(antinode_2_x, antinode_2_y)):
            antinodes.add(
                Antinode(
                    frequency=antenna_1.frequency,
                    position=Coordinate(antinode_2_x, antinode_2_y),
                )
            )

            antinode_2_x += distance_x
            antinode_2_y += distance_y

        return antinodes

    def get_antinodes(self, resonance=False) -> Set[Antinode]:

        antinodes: Set[Antinode] = set()

        for _, antennas in self.get_antennas_by_frequency().items():
            for antenna_1, antenna_2 in combinations(antennas, 2):

                if resonance:
                    antinodes = antinodes.union(
                        self.get_antinodes_for_antennas_resonance(antenna_1, antenna_2)
                    )
                else:
                    antinodes = antinodes.union(
                        self.get_antinodes_for_antennas(antenna_1, antenna_2)
                    )

        return antinodes


def parse_grid(file_path: Path) -> List[str]:

    grid = []

    with open(file_path, mode="r") as file:
        for line in file.readlines():
            grid.append(line.strip("\n"))

    return grid


if __name__ == "__main__":

    grid_parsed = parse_grid(Path("day_8_input.txt"))

    grid = Grid(grid_parsed)

    antinodes = grid.get_antinodes(resonance=False)

    unique_positions = {a.position for a in antinodes}

    print(
        f"{len(antinodes)} antinodes present in the grid in {len(unique_positions)} unique positions"
    )

    for p in unique_positions:
        if grid_parsed[p.y][p.x] == ".":
            grid_parsed[p.y] = (
                grid_parsed[p.y][: p.x] + "#" + grid_parsed[p.y][p.x + 1 :]
            )

    print(grid_parsed)
