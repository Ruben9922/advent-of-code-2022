from collections.abc import Generator


def parse_ranges(puzzle_input: list[str]) -> Generator[tuple[set[int], set[int]], None, None]:
    return ((set(range(int(x.split(",")[0].split("-")[0]), int(x.split(",")[0].split("-")[1]) + 1)),
             set(range(int(x.split(",")[1].split("-")[0]), int(x.split(",")[1].split("-")[1]) + 1))) for x in puzzle_input)


def day_4_puzzle_1(puzzle_input: list[str]) -> None:
    ranges = parse_ranges(puzzle_input)
    is_subset = [r[0] <= r[1] or r[1] <= r[0] for r in ranges]
    print(is_subset.count(True))


def day_4_puzzle_2(puzzle_input: list[str]) -> None:
    ranges = parse_ranges(puzzle_input)
    is_overlap = [bool(r[0] & r[1]) for r in ranges]
    print(is_overlap.count(True))


if __name__ == "__main__":
    print("Enter or paste your content. Ctrl-D / Cmd-D to finish inputting.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    day_4_puzzle_1(contents)
    day_4_puzzle_2(contents)
