from collections import deque
from pathlib import Path
import re
from typing import Dict, List, Tuple


def read_input() -> List[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split('.')[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file, "r") as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


def get_state_and_instructions(input: List[str]) -> Tuple[List[str], List[str]]:
    split_index = None
    for index, line in enumerate(input):
        if not line:
            split_index = index
            break
    return input[:split_index], input[split_index + 1:]


def get_starter_crate_stacks(input: List[str]) -> Dict[int, deque]:
    crate_stacks = dict()
    for index, line in enumerate(input[::-1]):
        # create deques per stack identifier
        if index == 0:
            stack_ids: List[int] = [int(stack_id) for stack_id in line.split(" ") if stack_id]
            for stack_id in stack_ids:
                crate_stacks[stack_id] = deque()
            continue
        # each crate id takes us 3 chars with 1 char in-between
        #  thus, we can look at every 4th index, starting on index 1.
        # then, add crates to their respective stack.
        for stack_id, crate in enumerate(line[1::4], 1):
            if not crate.strip():
                continue
            crate_stacks[stack_id].append(crate)
    return crate_stacks


def apply_instructions(crate_stacks: Dict[int, deque], instructions: List[str], can_move_multi=False) -> Dict[int, deque]:
    regex = re.compile(r"move (?P<qty>\d.*) from (?P<src>\d.*) to (?P<dst>\d.*)")
    for step in instructions:
        matches = re.match(regex, step)
        src = int(matches.group("src"))
        dst = int(matches.group("dst"))
        qty = int(matches.group("qty"))
        tmp_deque = deque()
        for _ in range(qty):
            tmp_deque.append(crate_stacks[src].pop())
        if can_move_multi:
            # keep the original order, thus reverse the tmp deque before extending
            tmp_deque.reverse()
        crate_stacks[dst].extend(tmp_deque)
    return crate_stacks


def get_top_crates(crate_stacks: Dict[int, deque]) -> str:
    top_crates = list()
    for _, stack in crate_stacks.items():
        top_crates.append(stack[-1])
    return "".join(top_crates)


def run_part_1(input: List[str]) -> str:
    input_state, input_instructions = get_state_and_instructions(input)
    crate_stacks = get_starter_crate_stacks(input_state)
    apply_instructions(crate_stacks, input_instructions, can_move_multi=False)
    top_crates: str = get_top_crates(crate_stacks)
    return top_crates


def run_part_2(input: List[str]) -> str:
    input_state, input_instructions = get_state_and_instructions(input)
    crate_stacks = get_starter_crate_stacks(input_state)
    apply_instructions(crate_stacks, input_instructions, can_move_multi=True)
    top_crates: str = get_top_crates(crate_stacks)
    return top_crates


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))  # SBPQRSCDF - correct
    print(run_part_2(input))  # RGLVRCQSB - correct
