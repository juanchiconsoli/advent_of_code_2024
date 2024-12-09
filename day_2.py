from itertools import pairwise
from pathlib import Path
from typing import List
from rich import print

Report = List[int]


def parse_input(file: Path) -> List[Report]:
    reports = []

    if not file.exists():
        raise FileNotFoundError(f"file {file} didn't exist")

    with open(file, mode="r") as reports_file:
        for line in reports_file.readlines():
            report = line.split(" ")
            report_clean = [int(x.strip().strip("\n")) for x in report]
            reports.append(report_clean)

    return reports


def is_valid(report: Report):

    return is_increasing_or_decreasing(report)


def is_increasing_or_decreasing(report: Report):
    return is_all_increasing(report) or is_all_decreasing(report)


def is_all_increasing(report: Report):
    return all(
        (a < b) and (abs(b - a) >= 1 and abs(a - b) <= 3) for a, b in pairwise(report)
    )


def is_all_decreasing(report: Report):
    return all(
        (a > b) and (abs(b - a) >= 1 and abs(a - b) <= 3) for a, b in pairwise(report)
    )


if __name__ == "__main__":

    valid_reports = []

    reports = parse_input(Path("./day_2_input.txt"))

    for report in reports:

        report_to_evaluate = [report[:i] + report[i + 1 :] for i in range(len(report))]

        report_to_evaluate += [[x for x in report]]

        if any(is_valid(r) for r in report_to_evaluate):
            valid_reports.append(report)

    print(
        f"Analizamos {len(reports)} ecuaciones de las cuales {len(valid_reports)} eran validas."
    )
