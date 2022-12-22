from pathlib import Path


def read_input() -> list[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split(".")[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file) as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


def run_part_1(input: list[str]) -> int:
    pass


def run_part_2(input: list[str]) -> int:
    pass


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))
    print(run_part_2(input))
