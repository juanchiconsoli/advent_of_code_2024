# garden has plants indicated with a letter.
# when gardein_plots are touching horizontally or veritcally they form a region
# calculare region area or perimeter
# area: number of plants the garden_plot contains
# perimeter: number of sides of garden plots in the region that do not touch another garden_plot in the same region
# price of fence for region = area * perimeter
# total price = sum of all region prices

from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, NamedTuple, Set
from rich import print


class Coordinate(NamedTuple):
    row: int
    column: int


class GardenPlot(NamedTuple):
    plant: str
    position: Coordinate


class Region:

    def __init__(self, garden_plots: Set[GardenPlot], plant: str):
        self._garden_plots = garden_plots
        self._garden_plot_coordinates = [x.position for x in self._garden_plots]
        self._garden_plot_coordinates.sort(key=lambda x: (x.row, x.column))
        self._plant = plant

        self._area = len(self._garden_plots)
        self._perimeter = self._calculate_perimeter()
        self._perimeter_discount = self._calculate_perimeter_with_discount()

    def get_area(self):
        return self._area

    def get_perimeter(self):
        return self._perimeter

    def get_perimeter_discount(self):
        return self._perimeter_discount

    def get_price(self):
        return self._area * self._perimeter

    def get_price_with_discount(self):
        return self._area * self._perimeter_discount

    def _calculate_perimeter(self) -> int:
        perimeter = 0

        for plot in self._garden_plots:
            # Check each side of the current coordinate
            for neighbor in self._get_coordinate_neighbors(plot.position):

                if neighbor not in self._garden_plot_coordinates:
                    # If no neighbor exists, this side contributes to the perimeter
                    perimeter += 1

        return perimeter

    def _calculate_perimeter_with_discount(self) -> int:
        return self._perimeter

    def _get_coordinate_neighbors(self, coord: Coordinate):

        return {
            Coordinate(coord.row - 1, coord.column),  # up
            Coordinate(coord.row + 1, coord.column),  # down
            Coordinate(coord.row, coord.column - 1),  # left
            Coordinate(coord.row, coord.column + 1),  # right
        }

    def _are_adjacent(self, coord1: Coordinate, coord2: Coordinate):
        """Check if two coordinates are adjacent (horizontally or vertically)."""
        return (
            coord1.row == coord2.row and abs(coord1.column - coord2.column) == 1
        ) or (coord1.column == coord2.column and abs(coord1.row - coord2.row) == 1)

    def __repr__(self):
        return f"Region(plant='{self._plant}', area={self.get_area()}, perimeter={self.get_perimeter()}, perimeter_discount={self.get_perimeter_discount()})"


class Garden:

    def __init__(self, grid: List[str]):
        self.grid = grid
        self.column_max = len(self.grid[0])
        self.row_max = len(self.grid)

    def is_coordinate_within_limits(self, coordinate: Coordinate):

        return coordinate.row in range(self.row_max) and coordinate.column in range(
            self.column_max
        )

    def get_next_step_possible_positions(
        self, plant: str, current_position: Coordinate
    ) -> List[Coordinate]:

        right = Coordinate(current_position.row, current_position.column + 1)
        down = Coordinate(current_position.row + 1, current_position.column)
        left = Coordinate(current_position.row, current_position.column - 1)
        up = Coordinate(current_position.row - 1, current_position.column)

        return [
            x
            for x in [right, down, left, up]
            if self.is_coordinate_within_limits(x)
            and self.grid[x.row][x.column] == plant
        ]

    def get_plant(self, position: Coordinate):
        if not self.is_coordinate_within_limits(position):
            raise ValueError("Coordinate off grid")

        return self.grid[position.row][position.column]


def parse_garden(file_path: Path):

    garden = []

    with open(file_path, mode="r") as file:
        for line in file.readlines():
            garden.append(line.strip("\n"))

    return Garden(garden)


if __name__ == "__main__":

    garden = parse_garden(Path("./day_12_input.txt"))

    visited: Set[Coordinate] = set()
    regions: List[Region] = []

    for r in range(garden.row_max):
        for c in range(garden.column_max):
            current_region = set()

            current_position = Coordinate(r, c)
            plant = garden.get_plant(current_position)

            stack = deque([current_position])

            while stack:
                pos = stack.popleft()

                if pos in visited:
                    continue

                current_region.add(GardenPlot(plant, pos))
                visited.add(pos)

                for next_pos in garden.get_next_step_possible_positions(plant, pos):
                    stack.append(next_pos)

            if len(current_region) > 0:
                regions.append(Region(current_region, plant))

    print(
        f"{len(regions)} garden plots regions found in the garden. The sum of all region prices is {sum(r.get_price() for r in regions)} with discount {sum(r.get_price_with_discount() for r in regions)}"
    )

    print(regions[:5])
