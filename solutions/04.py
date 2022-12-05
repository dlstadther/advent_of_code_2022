from pathlib import Path
import re
from typing import List, Set, Tuple


def read_input() -> List[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split('.')[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file, "r") as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


def get_assignments(line: str) -> Tuple[str, str]:
    assignment_1, assignment_2 = line.split(",", 1)
    return assignment_1, assignment_2


def parse_range(section_range: str) -> Set[int]:
    regex = re.compile(r"(?P<index_start>\d.*)-(?P<index_end>\d.*)")
    matches = re.match(regex, section_range)
    index_start, index_end = int(matches.group("index_start")), int(matches.group("index_end"))
    sections = [section for section in range(index_start, index_end + 1)]
    return set(sections)


def is_assignment_fully_contained(assignment_1: Set[int], assignment_2: Set[int]) -> bool:
    return assignment_1.issuperset(assignment_2) or assignment_2.issuperset(assignment_1)


def run_part_1(input: List[str]) -> int:
    qty_fully_contained = 0
    for line in input:
        a1, a2 = get_assignments(line)
        a1_range = parse_range(a1)
        a2_range = parse_range(a2)
        qty_fully_contained += int(is_assignment_fully_contained(a1_range, a2_range))
    return qty_fully_contained


def do_assignments_overlap(assignment_1: Set[int], assignment_2: Set[int]) -> bool:
    return not assignment_1.isdisjoint(assignment_2)


def run_part_2(input: List[str]) -> int:
    qty_overlapping = 0
    for line in input:
        a1, a2 = get_assignments(line)
        a1_range = parse_range(a1)
        a2_range = parse_range(a2)
        qty_overlapping += int(do_assignments_overlap(a1_range, a2_range))
    return qty_overlapping


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))  # 588 - correct
    print(run_part_2(input))  # 911 - correct
