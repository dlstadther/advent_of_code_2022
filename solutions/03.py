from pathlib import Path
from typing import Generator, List, Set, Tuple


def read_input() -> List[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split('.')[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file, "r") as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


def get_compartments(line: str) -> Tuple[str, str]:
    position = len(line) // 2
    return line[:position], line[position:]


def find_intersection(*sets: Set) -> Set:
    return set.intersection(*sets)


def char_to_priority(char: str) -> int:
    # a-z = 1-26
    # A-Z = 27-52
    is_cap = char.isupper()
    if is_cap:
        value = ord(char) - ord("A") + 27
    else:
        value = ord(char) - ord("a") + 1
    return value


def run_part_1(input: List[str]) -> int:
    total_priority = sum([
        char_to_priority(find_intersection(
            *[set(comp) for comp in get_compartments(line)]
        ).pop()) for line in input
    ])
    return total_priority


def group_rucksacks(input: List[str]) -> Generator[str, None, None]:
    group_size = 3
    for index in range(0, len(input) + 1 - group_size, group_size):
        start_index = index
        end_index = index + group_size
        yield input[start_index:end_index]


def run_part_2(input: List[str]) -> int:
    total_priority = 0
    for rucksacks in group_rucksacks(input):
        rucksack_sets = [set(r) for r in rucksacks]
        badge = find_intersection(*rucksack_sets)
        assert len(badge) == 1
        total_priority += char_to_priority(badge.pop())
    return total_priority


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))  # 8185 - correct
    print(run_part_2(input))  # 2817 - correct
