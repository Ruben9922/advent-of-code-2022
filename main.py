def day_1_puzzle_1(puzzle_input):
    elves_calories = [[int(elf_calorie) for elf_calorie in elf_string.split("\n")] for elf_string in puzzle_input.split("\n\n")]
    elf_with_most_calories = max(sum(elf_calories) for elf_calories in elves_calories)
    print(elf_with_most_calories)


def day_1_puzzle_2(puzzle_input):
    elves_calories = ((int(elf_calorie) for elf_calorie in elf_string.split("\n")) for elf_string in
                      puzzle_input.split("\n\n"))
    elves_calories_sum = [sum(elf_calories) for elf_calories in elves_calories]
    elves_with_most_calories = []
    for _ in range(3):
        next_elf_with_most_calories = max(elves_calories_sum)
        elves_with_most_calories.append(next_elf_with_most_calories)
        elves_calories_sum.remove(next_elf_with_most_calories)
    print(sum(elves_with_most_calories))


if __name__ == "__main__":
    print("Enter or paste your content. Ctrl-D / Cmd-D to finish inputting.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    day_1_puzzle_1("\n".join(contents))  # Bit of a hack lol
    day_1_puzzle_2("\n".join(contents))  # Bit of a hack lol
