from collections.abc import Generator


def split_input(puzzle_input: list[str]) -> tuple[list[str], list[str]]:
    index = 0
    for line in puzzle_input:
        if not line:
            break
        index += 1
    return puzzle_input[:index], puzzle_input[index + 1:]


def parse_stacks(stack_strings: list[str]) -> list[list[str]]:
    return [[char for char in stack if char != " "] for stack in zip(*stack_strings[:-1])
            if not all(char == "[" or char == "]" or char == " " for char in stack)]


class Instruction:
    def __init__(self, quantity: int, from_stack_index: int, to_stack_index: int):
        self.quantity = quantity
        self.from_stack_index = from_stack_index
        self.to_stack_index = to_stack_index


def parse_instructions(instruction_strings: list[str]) -> Generator[Instruction, None, None]:
    return (Instruction(
        quantity=int(instruction_string.split(" ")[1]),
        from_stack_index=int(instruction_string.split(" ")[3]) - 1,
        to_stack_index=int(instruction_string.split(" ")[5]) - 1,
    ) for instruction_string in instruction_strings)


def day_5(puzzle_input: list[str], crates_reversed_when_moved: bool) -> None:
    stack_strings, instruction_strings = split_input(puzzle_input)
    stacks = parse_stacks(stack_strings)
    instructions = parse_instructions(instruction_strings)
    for instruction in instructions:
        moved_crates = stacks[instruction.from_stack_index][:instruction.quantity]
        if crates_reversed_when_moved:
            moved_crates = list(reversed(moved_crates))
        stacks[instruction.from_stack_index] = stacks[instruction.from_stack_index][instruction.quantity:]
        stacks[instruction.to_stack_index] = moved_crates + stacks[instruction.to_stack_index]
    print("".join(stack[0] for stack in stacks))


def day_5_puzzle_1(puzzle_input: list[str]) -> None:
    day_5(puzzle_input, True)


def day_5_puzzle_2(puzzle_input: list[str]) -> None:
    day_5(puzzle_input, False)


if __name__ == "__main__":
    print("Enter or paste your content. Ctrl-D / Cmd-D to finish inputting.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    day_5_puzzle_1(contents)
    day_5_puzzle_2(contents)
