import itertools
from collections.abc import Generator
from typing import TypeVar

T = TypeVar("T")


def get_item_priority(item: str) -> int:
    if "A" <= item <= "Z":
        return ord(item) - ord("A") + 27
    elif "a" <= item <= "z":
        return ord(item) - ord("a") + 1
    else:
        return 0


def day_3_puzzle_1(puzzle_input: list[str]) -> None:
    common_items = ((set(line[:len(line) // 2]).intersection(set(line[len(line) // 2:]))) for line in puzzle_input)
    common_items_flattened = itertools.chain.from_iterable(common_items)
    common_item_priorities = (get_item_priority(item) for item in common_items_flattened)
    total_priority = sum(common_item_priorities)
    print(total_priority)


def chunks(list: list[T], chunk_size: int) -> Generator[list[str], None, None]:
    return (list[i:i + chunk_size] for i in range(0, len(list), chunk_size))


def day_3_puzzle_2(puzzle_input: list[str]) -> None:
    rucksacks_by_group = chunks(puzzle_input, 3)
    badges_by_group = (set.intersection(*(set(rucksack) for rucksack in group_rucksacks))
                       for group_rucksacks in rucksacks_by_group)
    badges = itertools.chain.from_iterable(badges_by_group)
    badge_priorities = (get_item_priority(badge) for badge in badges)
    total_priority = sum(badge_priorities)
    print(total_priority)


if __name__ == "__main__":
    print("Enter or paste your content. Ctrl-D / Cmd-D to finish inputting.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    day_3_puzzle_1(contents)
    day_3_puzzle_2(contents)
