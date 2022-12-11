from pathlib import Path
from typing import List, Tuple


def read_input() -> List[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split('.')[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file, "r") as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


def calculate_x_at_each_step(input: List[str], starting_value: int = 1) -> List[int]:
    x_values = [starting_value]
    for line in input:
        current_value = x_values[-1]
        if line == "noop":
            x_values.append(current_value)
        elif line.startswith("addx"):
            val = int(line.split()[1])
            next_value = current_value + val
            x_values.append(current_value)
            x_values.append(next_value)
        else:
            raise ValueError(f"Unexpected command: {line}")
    return x_values


def run_part_1(input: List[str]) -> int:
    poi_indicies = [20, 60, 100, 140, 180, 220]
    x_values = calculate_x_at_each_step(input=input, starting_value=1)
    total_poi_values = 0
    for poi in poi_indicies:
        # handle offset by 1 when accessing values
        total_poi_values += (poi * x_values[poi - 1])
    return total_poi_values


def get_sprite_pos_x(val: int, length: int) -> int:
    return val - (length // 2)


def calculate_cycle_position(cycle: int, row_len: int) -> Tuple[int, int]:
    return divmod(cycle, row_len)


def update_crt(crt_map: List[List[str]], cycle_values: List[int], sprite_len: int, crt_row_len: int) -> List[List[str]]:
    for cycle, x in enumerate(cycle_values):
        sprite_start = get_sprite_pos_x(val=x, length=sprite_len)
        sprite_end = sprite_start + sprite_len - 1
        pos_x, pos_y = calculate_cycle_position(cycle=cycle, row_len=crt_row_len)
        if sprite_start <= pos_y <= sprite_end:
            crt_map[pos_x][pos_y] = "#"
    return crt_map


def print_crt(pixels: List[List[str]]) -> None:
    for row in pixels:
        print(" ".join(row))


def run_part_2(input: List[str]) -> None:
    len_of_sprite = 3
    len_of_row = 40
    qty_rows = 6
    crt = [list(".") * len_of_row for _ in range(qty_rows)]
    cycle_values = calculate_x_at_each_step(input=input, starting_value=1)
    crt = update_crt(crt_map=crt, cycle_values=cycle_values, sprite_len=len_of_sprite, crt_row_len=len_of_row)
    print_crt(pixels=crt)


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))  # 14340 - correct
    print(run_part_2(input))  # PAPJCBHP - correct
