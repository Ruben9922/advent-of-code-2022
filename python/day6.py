from collections.abc import Sequence


def all_unique(seq: Sequence) -> bool:
    return len(seq) == len(set(seq))


def get_index_after_marker(string: str, marker_length: int) -> int:
    for index in range(len(string)):
        if index >= marker_length - 1:
            possible_marker = string[index - marker_length + 1: index + 1]
            if all_unique(possible_marker):
                return index


def day_6_puzzle_1(puzzle_input: str) -> None:
    print(get_index_after_marker(puzzle_input, 4) + 1)


def day_6_puzzle_2(puzzle_input: str) -> None:
    print(get_index_after_marker(puzzle_input, 14) + 1)


if __name__ == "__main__":
    puzzle_input = input()
    day_6_puzzle_1(puzzle_input)
    day_6_puzzle_2(puzzle_input)
