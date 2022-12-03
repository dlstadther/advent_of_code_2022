from pathlib import Path

filepath = Path(__file__).resolve()
filename_no_ext = filepath.name.split('.')[0]
filedir = filepath.parent
input_file = filedir / f"../inputs/{filename_no_ext}.txt"

if __name__ == "__main__":
    map: dict = dict()
    elf_index = 1
    with open(input_file, "r") as infile:
        for line in infile:
            line = line.strip()
            if line == "":
                elf_index += 1
            else:
                if map.get(elf_index) is None:
                    map[elf_index] = 0
                map[elf_index] += int(line)
    map_sorted = [v for k, v in sorted(map.items(), key=lambda item: item[1], reverse=True)]
    single_most = map_sorted[0]
    print(single_most)  # 69795 - correct
    top_most = sum(map_sorted[0:3])
    print(top_most)  # 208437 - correct
