from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import List, NamedTuple
from rich import print

# topographic_map, grid of coordinates and their height
# hiking_trail up, down, left, right start in 0 end in 9, each step increases by 1+
# trailhead trailhead: any position that starts one or more hiking trails. always height 0
# trail_head_score = number of 9-height positions reachable from that trailhead via a hiking trail


class Coordinate(NamedTuple):
    row: int
    column: int


@dataclass
class TrailHead:
    position: Coordinate
    score: int


class TopographicMap:

    def __init__(self, grid: List[str]):
        self.grid = grid
        self.column_max = len(self.grid[0])
        self.row_max = len(self.grid)

    def is_coordinate_within_limits(self, coordinate: Coordinate):

        return coordinate.row in range(self.row_max) and coordinate.column in range(
            self.column_max
        )

    def get_trailhead_scores(self, rating_scale=False):

        trailhead_scores = []

        for row in range(self.row_max):
            for col in range(self.column_max):

                height = self.grid[row][col]

                if height == 9:
                    if rating_scale:
                        score = self.calculate_rating(Coordinate(row, col))
                    else:
                        score = self.calculate_score(Coordinate(row, col))

                    if score > 0:
                        trailhead_scores.append(score)

        return trailhead_scores

    def calculate_score(self, trail_end: Coordinate):
        trails = 0
        stack = deque([trail_end])
        seen = set()

        while stack:
            pos = stack.popleft()
            height = self.grid[pos.row][pos.column]

            if pos in seen:
                continue

            seen.add(pos)

            if height == 0:
                trails += 1

            for next_pos in self.get_next_step_possible_positions(height, pos):
                stack.append(next_pos)

        return trails

    def calculate_rating(self, trail_end: Coordinate):
        DP = {}

        if self.grid[trail_end.row][trail_end.column] == 0:
            return 1
        if trail_end in DP:
            return DP[trail_end]

        trails = 0
        for next_pos in self.get_next_step_possible_positions(
            self.grid[trail_end.row][trail_end.column], trail_end
        ):

            trails += self.calculate_rating(next_pos)

        DP[trail_end] = trails

        return trails

    def get_next_step_possible_positions(
        self, current_height: int, current_position: Coordinate
    ) -> List[Coordinate]:

        right = Coordinate(current_position.row, current_position.column + 1)
        down = Coordinate(current_position.row + 1, current_position.column)
        left = Coordinate(current_position.row, current_position.column - 1)
        up = Coordinate(current_position.row - 1, current_position.column)

        return [
            x
            for x in [right, down, left, up]
            if self.is_coordinate_within_limits(x)
            and self.grid[x.row][x.column] == current_height - 1
        ]


def read_topographic_map(file_path: Path) -> TopographicMap:

    topographic_map = []

    with open(file_path, mode="r") as file:
        for line in file.readlines():
            topographic_map.append(line.strip("\n"))

    return TopographicMap([[int(x) for x in row] for row in topographic_map])


if __name__ == "__main__":

    topographic_map = read_topographic_map(Path("./day_10_input.txt"))

    trailhead_scores = topographic_map.get_trailhead_scores(rating_scale=True)

    print(
        f"Found {len(trailhead_scores)} trails the trail head scores is {sum(x for x in trailhead_scores)}"
    )
