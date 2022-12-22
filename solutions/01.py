from pathlib import Path


def read_input() -> list[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split(".")[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file) as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


def get_aggregate_calories_desc(input: list[str]) -> list[int]:
    calories = list()
    calorie_counter = 0
    for line in input:
        if not line:
            calories.append(calorie_counter)
            calorie_counter = 0
            continue
        calorie_counter += int(line)
    calories_desc = sorted(calories, reverse=True)
    return calories_desc


def run_part_1(input: list[str]) -> int:
    return get_aggregate_calories_desc(input)[0]


def run_part_2(input: list[str]) -> int:
    return sum(get_aggregate_calories_desc(input)[0:3])


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))  # 69795 - correct
    print(run_part_2(input))  # 208437 - correct
