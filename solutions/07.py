from pathlib import Path
import re
from typing import Dict, List


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name: str, parent: "Directory" = None):
        self.name = name
        self.parent = parent
        self.files: Dict[str, File] = dict()
        self.directories: Dict[str, "Directory"] = dict()

    @property
    def size(self) -> int:
        total_file_size = sum([f.size for _, f in self.files.items()])
        total_nested_size = sum([d.size for _, d in self.directories.items()])
        return total_nested_size + total_file_size

    def reset(self):
        self.files = dict()
        self.directories = dict()

    def add_file(self, file: File):
        self.files[file.name] = file

    def add_directory(self, directory: "Directory"):
        self.directories[directory.name] = directory

    def __ge__(self, other: "Directory"):
        return self.size >= other.size

    def __gt__(self, other: "Directory"):
        return self.size > other.size

    def __lt__(self, other: "Directory"):
        return self.size < other.size

    def __le__(self, other: "Directory"):
        return self.size < other.size

    def __str__(self):
        if self.parent:
            return f"{self.__class__.__name__}(name={self.name}, size={self.size}, parent={self.parent.name})"
        else:
            return f"{self.__class__.__name__}(name={self.name}, size={self.size})"

    def __repr__(self):
        if self.parent:
            return f"{self.__class__.__name__}(name={self.name}, size={self.size}, parent={self.parent.name})"
        else:
            return f"{self.__class__.__name__}(name={self.name}, size={self.size})"


def read_input() -> List[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split('.')[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file, "r") as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


# def is_command(input: str) -> bool:
#     return bool(input.startswith("$ "))


def generate_filesystem_from_commands(input: List[str]) -> Directory:
    regex_cd_dir = re.compile(r"\$ cd (?P<name>.*)")
    regex_ls_item = re.compile(r"(?P<dir_or_size>dir|\d.*) (?P<name>.*)")
    root_dir: Directory = None
    cwd: Directory = None
    for i, line in enumerate(input, 1):
        # cd root
        if line == "$ cd /":
            # create root if DNE
            if root_dir is None:
                root_dir = Directory(name="/")
            cwd = root_dir
        # cd parent
        elif line == "$ cd ..":
            cwd = cwd.parent
        # cd to specific dir
        elif line.startswith("$ cd"):
            # print(f"Moving away from dir - {cwd}")
            matches = re.match(regex_cd_dir, line)
            dir_name = matches.group("name")
            tmp_dir = cwd.directories.get(dir_name)
            cwd = tmp_dir
        # list cwd contents
        elif line.startswith("$ ls"):
            # reset dir and file content of cwd
            cwd.reset()
        # content of cwd
        else:
            matches = re.match(regex_ls_item, line)
            dir_or_size = matches.group("dir_or_size")
            name = matches.group("name")
            if dir_or_size == "dir":
                tmp_dir = Directory(name=name, parent=cwd)
                cwd.add_directory(tmp_dir)
            else:
                tmp_file = File(name=name, size=int(dir_or_size))
                cwd.add_file(tmp_file)
    return root_dir


def get_dirs(root_dir: Directory) -> List[Directory]:
    # effectively a tree/graph traversal algorithm
    dirs: List[Directory] = list()
    dirs_to_visit: List[Directory] = [root_dir]

    while dirs_to_visit:
        tmp_dir = dirs_to_visit.pop(0)
        if tmp_dir not in dirs:
            dirs.append(tmp_dir)
        directories = [d for _, d in tmp_dir.directories.items()]
        dirs_to_visit.extend(directories)
    return dirs


def run_part_1(input: List[str]) -> int:
    root_dir = generate_filesystem_from_commands(input=input)
    dirs = get_dirs(root_dir=root_dir)
    dirs_sorted = sorted(dirs)
    max_allowed_size = 100000
    total_size = 0
    for d in dirs_sorted:
        if d.size > max_allowed_size:
            break
        total_size += d.size
    return total_size


def run_part_2(input: List[str]) -> int:
    max_fs_size = 70000000
    min_unused_size = 30000000
    root_dir = generate_filesystem_from_commands(input=input)
    dirs = get_dirs(root_dir=root_dir)
    dirs_sorted = sorted(dirs)
    remaining_size = max_fs_size - dirs_sorted[-1].size
    min_size_to_remove = min_unused_size - remaining_size
    for d in dirs_sorted:
        if d.size > min_size_to_remove:
            return d.size


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))  # 1743217 - correct
    print(run_part_2(input))  # 8319096 - correct
