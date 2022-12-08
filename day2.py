from enum import Enum
from typing import Optional

Shape = Enum("Shape", ["ROCK", "PAPER", "SCISSORS"])
shape_to_index = dict((shape, index) for index, shape in enumerate(Shape))
index_to_shape = dict((index, shape) for index, shape in enumerate(Shape))


def parse_opponent_selected_shape(shape_string: str) -> Optional[Shape]:
    match shape_string:
        case "A":
            return Shape.ROCK
        case "B":
            return Shape.PAPER
        case "C":
            return Shape.SCISSORS
        case _:
            return None


def parse_own_selected_shape(shape_string: str) -> Optional[Shape]:
    match shape_string:
        case "X":
            return Shape.ROCK
        case "Y":
            return Shape.PAPER
        case "Z":
            return Shape.SCISSORS
        case _:
            return None


def compute_shape_score(shape: Optional[Shape]) -> int:
    match shape:
        case Shape.ROCK:
            return 1
        case Shape.PAPER:
            return 2
        case Shape.SCISSORS:
            return 3
        case _:
            return 0


def compute_outcome_score(round: tuple[Optional[Shape], Optional[Shape]]) -> int:
    match (shape_to_index[round[1]] - shape_to_index[round[0]]) % 3:
        case 0:  # Draw
            return 3
        case 1:  # Win
            return 6
        case 2:
            return 0


def compute_score(round: tuple[Optional[Shape], Optional[Shape]]) -> int:
    shape_score = compute_shape_score(round[1])
    outcome_score = compute_outcome_score(round)
    return shape_score + outcome_score


def day_2_puzzle_1(puzzle_input: list[str]) -> None:
    strategy_guide = ((
        parse_opponent_selected_shape(line.split()[0]),
        parse_own_selected_shape(line.split()[1]),
    ) for line in puzzle_input)

    scores = (compute_score(round) for round in strategy_guide)
    total_score = sum(scores)
    print(total_score)


Outcome = Enum("Outcome", ["WIN", "LOSE", "DRAW"])


def parse_outcome(outcome_string: str) -> Optional[Outcome]:
    match outcome_string:
        case "X":
            return Outcome.LOSE
        case "Y":
            return Outcome.DRAW
        case "Z":
            return Outcome.WIN
        case _:
            return None


def infer_own_selected_shape_from_outcome(round: tuple[Optional[Shape], Optional[Outcome]])\
        -> tuple[Optional[Shape], Optional[Shape]]:
    match round[1]:
        case Outcome.WIN:
            return round[0], index_to_shape[((shape_to_index[round[0]] + 1) % 3)]
        case Outcome.LOSE:
            return round[0], index_to_shape[((shape_to_index[round[0]] + 2) % 3)]
        case Outcome.DRAW:
            return round[0], round[0]


def day_2_puzzle_2(puzzle_input: list[str]) -> None:
    strategy_guide = ((
        parse_opponent_selected_shape(line.split()[0]),
        parse_outcome(line.split()[1]),
    ) for line in puzzle_input)

    scores = (compute_score(infer_own_selected_shape_from_outcome(round)) for round in strategy_guide)
    total_score = sum(scores)
    print(total_score)


if __name__ == "__main__":
    print("Enter or paste your content. Ctrl-D / Cmd-D to finish inputting.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    day_2_puzzle_1(contents)
    day_2_puzzle_2(contents)
