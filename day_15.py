import re
from collections import deque
from rich import print


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up right down left
DIRECTION_MAPPTING = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


def ints(s):
    return [int(x) for x in re.findall("-?\d+", s)]


DATA = open("day_15_input.txt").read().strip()

GRID, instructions = DATA.split("\n\n")
GRID = GRID.split("\n")


def solve(MAP, part2):
    row_max = len(MAP)
    col_max = len(MAP[0])
    MAP = [[GRID[r][c] for c in range(col_max)] for r in range(row_max)]

    if part2:
        BIG_G = []
        for r in range(row_max):
            row = []
            for c in range(col_max):
                if MAP[r][c] == "#":
                    row.append("#")
                    row.append("#")
                if MAP[r][c] == "O":
                    row.append("[")
                    row.append("]")
                if MAP[r][c] == ".":
                    row.append(".")
                    row.append(".")
                if MAP[r][c] == "@":
                    row.append("@")
                    row.append(".")
            BIG_G.append(row)
        MAP = BIG_G
        col_max *= 2

    for r in range(row_max):
        for c in range(col_max):
            if MAP[r][c] == "@":
                robot_row, robot_column = r, c
                MAP[r][c] = "."

    r, c = robot_row, robot_column

    for inst in instructions:
        if inst == "\n":
            continue
        dr, dc = DIRECTION_MAPPTING[inst]

        rr, cc = r + dr, c + dc

        if MAP[rr][cc] == "#":
            continue
        elif MAP[rr][cc] == ".":
            r, c = rr, cc
        elif MAP[rr][cc] in ["[", "]", "O"]:
            Q = deque([(r, c)])
            SEEN = set()
            ok = True

            while Q:
                rr, cc = Q.popleft()
                if (rr, cc) in SEEN:
                    continue
                SEEN.add((rr, cc))
                rrr, ccc = rr + dr, cc + dc
                if MAP[rrr][ccc] == "#":
                    ok = False
                    break
                if MAP[rrr][ccc] == "O":
                    Q.append((rrr, ccc))
                if MAP[rrr][ccc] == "[":
                    Q.append((rrr, ccc))
                    assert MAP[rrr][ccc + 1] == "]"
                    Q.append((rrr, ccc + 1))
                if MAP[rrr][ccc] == "]":
                    Q.append((rrr, ccc))
                    assert MAP[rrr][ccc - 1] == "["
                    Q.append((rrr, ccc - 1))
            if not ok:
                continue
            while len(SEEN) > 0:
                for rr, cc in sorted(SEEN):
                    rrr, ccc = rr + dr, cc + dc
                    if (rrr, ccc) not in SEEN:
                        assert MAP[rrr][ccc] == "."
                        MAP[rrr][ccc] = MAP[rr][cc]
                        MAP[rr][cc] = "."
                        SEEN.remove((rr, cc))
            r = r + dr
            c = c + dc

    ans = 0
    for r in range(row_max):
        for c in range(col_max):
            if MAP[r][c] in ["[", "O"]:
                ans += 100 * r + c
    return ans


print(solve(GRID, False))
print(solve(GRID, True))
