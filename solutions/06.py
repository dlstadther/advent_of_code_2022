from collections import deque
from pathlib import Path


def read_input() -> list[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split(".")[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file) as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


def find_packet_start_index(signal: str, unique_sequence_len: int) -> int:
    tmp_sequence = deque(maxlen=unique_sequence_len)
    for index, char in enumerate(signal, 1):
        tmp_sequence.append(char)
        if index < unique_sequence_len:
            continue
        tmp_unique_len = set(tmp_sequence)
        if len(tmp_unique_len) == unique_sequence_len:
            return index


def run_part_1(input: list[str]) -> int:
    return find_packet_start_index(signal=input[0], unique_sequence_len=4)


def run_part_2(input: list[str]) -> int:
    return find_packet_start_index(signal=input[0], unique_sequence_len=14)


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))  # 1794 - correct
    print(run_part_2(input))  # 2851 - correct
