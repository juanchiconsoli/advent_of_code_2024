from pathlib import Path
from typing import List
from rich import print


def parse_grid(file_path: Path) -> List[str]:

    grid = []

    with open(file_path, mode="r") as file:
        for line in file.readlines():
            grid.append(line.strip("\n"))

    return grid


def count_appeareances_xmas(grid, word="XMAS"):

    rows = len(grid)
    cols = len(grid[0])

    word_len = len(word)

    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (0, -1),  # Left
        (-1, 0),  # Up
        (1, 1),  # Diagonal down-right
        (1, -1),  # Diagonal down-left
        (-1, 1),  # Diagonal up-right
        (-1, -1),  # Diagonal up-left
    ]

    def is_valid(x, y):
        """Check if the coordinates are within the grid."""
        return 0 <= x < rows and 0 <= y < cols

    def check_direction(x, y, dx, dy):
        """Check if the word exists in a specific direction."""
        for i in range(word_len):
            nx, ny = x + i * dx, y + i * dy
            if not is_valid(nx, ny) or grid[nx][ny] != word[i]:
                return False
        return True

    count = 0

    for x in range(rows):
        for y in range(cols):
            for direction_x, direction_y in directions:
                if check_direction(x, y, direction_x, direction_y):
                    count += 1
    return count


def count_cross_with_reversals(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # Function to check for a cross pattern with "MAS" or its reversed forms
    def is_cross(x, y):
        if (
            0 <= x - 1 < rows
            and 0 <= x + 1 < rows  # Top and bottom bounds
            and 0 <= y - 1 < cols
            and 0 <= y + 1 < cols  # Left and right bounds
            and grid[x][y] == "A"  # Center of the cross
            and (
                (
                    grid[x - 1][y - 1] == "M"
                    and grid[x + 1][y + 1] == "S"  # Top and bottom
                    and grid[x + 1][y - 1] == "M"
                    and grid[x - 1][y + 1] == "S"
                )  # Left and right
                or (
                    grid[x - 1][y - 1] == "S"
                    and grid[x + 1][y + 1] == "M"  # Flipped top and bottom
                    and grid[x + 1][y - 1] == "S"
                    and grid[x - 1][y + 1] == "M"
                )  # Flipped left and right
                or (
                    grid[x - 1][y - 1] == "M"
                    and grid[x + 1][y + 1] == "S"  # Vertical reversed
                    and grid[x + 1][y - 1] == "S"
                    and grid[x - 1][y + 1] == "M"
                )  # Horizontal reversed
                or (
                    grid[x - 1][y - 1] == "S"
                    and grid[x + 1][y + 1] == "M"  # Fully reversed
                    and grid[x + 1][y - 1] == "M"
                    and grid[x - 1][y + 1] == "S"
                )
            )
        ):
            return True
        return False

    # Scan the grid for the cross pattern
    for x in range(rows):
        for y in range(cols):
            if is_cross(x, y):
                count += 1

    return count


if __name__ == "__main__":

    grid = parse_grid(Path("day_4_input.txt"))

    result = count_cross_with_reversals(grid)

    print(f"Occurrences of 'MAS' in a cross 'X': {result}")
