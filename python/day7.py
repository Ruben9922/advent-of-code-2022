from abc import ABC
from enum import Enum, auto
from typing import Union, Optional


# {type: "output"} | {type: "input", command:{type:"cd"}}

class CommandType(Enum):
    ChangeDirectory = auto()
    List = auto()

class ChangeDirectoryCommandParameterType(Enum):
    MoveOut = auto()
    MoveIn = auto()
    MoveToRoot = auto()

class ChangeDirectoryCommandParameter(ABC):
    def __init__(self, parameter_type: ChangeDirectoryCommandParameterType) -> None:
        self.parameter_type = parameter_type

class ChangeDirectoryCommandMoveInParameter(ChangeDirectoryCommandParameter):
    def __init__(self, directory: str) -> None:
        super().__init__(ChangeDirectoryCommandParameterType.MoveIn)
        self.directory = directory

class ChangeDirectoryCommandMoveOutParameter(ChangeDirectoryCommandParameter):
    def __init__(self) -> None:
        super().__init__(ChangeDirectoryCommandParameterType.MoveOut)

class ChangeDirectoryCommandMoveToRootParameter(ChangeDirectoryCommandParameter):
    def __init__(self) -> None:
        super().__init__(ChangeDirectoryCommandParameterType.MoveToRoot)

class Command(ABC):
    def __init__(self, command_type: CommandType) -> None:
        self.command_type = command_type

class ChangeDirectoryCommand(Command):
    def __init__(self, parameter: ChangeDirectoryCommandParameter) -> None:
        super().__init__(CommandType.ChangeDirectory)
        self.parameter = parameter

class ListCommand(Command):
    def __init__(self) -> None:
        super().__init__(CommandType.List)

class ListCommandOutput(ABC):
    def __init__(self, file_item_type: FileItemType, name: str) -> None:
        self.file_item_type = file_item_type
        self.name = name

class ListCommandFileOutput(ListCommandOutput):
    def __init__(self, name: str, size: int) -> None:
        super().__init__(FileItemType.FILE, name)
        self.size = size

class ListCommandDirectoryOutput(ListCommandOutput):
    def __init__(self, name: str) -> None:
        super().__init__(FileItemType.DIRECTORY, name)


class FileItemType(Enum):
    FILE = auto()
    DIRECTORY = auto()


class Element(ABC):
    def __init__(self, name: str, element_type: FileItemType) -> None:
        self.name = name
        self.element_type = element_type
        self.parent: Optional[Element] = None


class FileElement(Element):
    def __init__(self, name: str, size: int) -> None:
        super().__init__(name, FileItemType.FILE)
        self.size = size


class DirectoryElement(Element):
    def __init__(self, name: str) -> None:
        super().__init__(name, FileItemType.DIRECTORY)
        self.children: dict[str, Element] = {}

    def add_child(self, child: "Element"):
        if child.name not in self.children:
            self.children[child.name] = child
            child.parent = self


def group_by_command_and_output(terminal_output: list[str]) -> list[tuple[str, list[str]]]:
    # grouped: list[tuple[str, list[str]]] = []
    tree = DirectoryElement("/")
    current = tree
    child_name: Optional[str] = None

    for line in terminal_output:
        line_tokens = line.split(None)

        if line_tokens[0] == "$":
            if line_tokens[1] == "cd":
                match line_tokens[2]:
                    case "/":
                        tree = DirectoryElement("/")
                        current = tree
                    case "..":
                        current = current.parent
                    case _:
                        current
            elif line_tokens[1] == "ls":
                pass
            else:
                print(f"Unrecognised command: \"{line_tokens[1]}\"")
                continue
        elif line_tokens[0] == "dir":
            name = line_tokens[1]
            current.add_child(DirectoryElement(name))
        else:
            size = int(line_tokens[0])
            name = line_tokens[1]
            current.add_child(FileElement(name, size))


    return tree

def parse_input(terminal_output: list[str]) -> list[Command | ListCommandOutput]:
    for line in terminal_output:
        match line.split():
            case ["cd", "/"]:



def day_7_puzzle_1(puzzle_input: list[str]) -> None:



if __name__ == "__main__":
    print("Enter or paste your content. Ctrl-D / Cmd-D to finish inputting.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    day_7_puzzle_1(contents)
    # day_5_puzzle_2(contents)
