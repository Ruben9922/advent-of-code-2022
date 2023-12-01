package main

import (
	"errors"
	"fmt"
	"log"
	"strconv"
	"strings"
)

//type fileType int
//
//const (
//	file fileType = iota
//	folder
//)
//
//type item struct {
//	name     string
//	fileType fileType
//	size     int
//}
//
//func newItem(name string, fileType fileType, size int) *item {
//	return &item{name: name, fileType: fileType, size: size}
//}
//
//type folderItem struct {
//	item
//	children map[string]item
//}
//
//func newFolderItem(name string, fileType fileType, size int, children map[string]item) *folderItem {
//	return &folderItem{item: *newItem(name, fileType, size), children: children}
//}

func main() {
	lines := readFileLines("input/day7.txt")

	commands, err := parse(lines)
	if err != nil {
		log.Fatal(err)
	}

	folderNodes, err := buildTree(commands)
	if err != nil {
		log.Fatal(err)
	}

	filteredFolderNodes := make([]*folderNode, 0, len(folderNodes))
	sum := 0
	for _, f := range folderNodes {
		size := f.getSize()
		if size <= 100000 {
			filteredFolderNodes = append(filteredFolderNodes, f)
			sum += size
		}
	}

	fmt.Println(sum)
}

type cdCommand struct {
	directory string
}

type cdParentCommand struct{}

type lsCommand struct {
	items []item
}

type commandType int

const (
	cdCommandType commandType = iota
	cdParentCommandType
	lsCommandType
)

type command interface {
	commandType() commandType
}

func (cc cdCommand) commandType() commandType {
	return cdCommandType
}

func (cc cdParentCommand) commandType() commandType {
	return cdParentCommandType
}

func (lc lsCommand) commandType() commandType {
	return lsCommandType
}

type folderItem struct {
	name string
}

type fileItem struct {
	name string
	size int
}

type itemType int

const (
	file itemType = iota
	folder
)

type item interface {
	itemType() itemType
}

func (fi fileItem) itemType() itemType {
	return file
}

func (fi folderItem) itemType() itemType {
	return folder
}

func parse(input []string) ([]command, error) {
	commands := make([]command, 0, 100) // todo update capacity
	for _, line := range input {
		tokens := strings.Split(line, " ")
		if tokens[0] == "$" {
			commandName := tokens[1]
			if commandName == "cd" {
				if tokens[2] == ".." {
					commands = append(commands, cdParentCommand{})
				} else {
					directory := tokens[2]
					commands = append(commands, cdCommand{directory: directory})
				}
			} else if commandName == "ls" {
				commands = append(commands, lsCommand{items: make([]item, 0, 10)})
			} else {
				return commands, errors.New(fmt.Sprintf("unrecognised command: %s", commandName))
			}
		} else if tokens[0] == "dir" {
			if len(commands) == 0 {
				return commands, errors.New("output with no preceding command")
			}

			currentCommand := &commands[len(commands)-1]
			if (*currentCommand).commandType() == lsCommandType { // todo: use type switch instead probably
				currentLsCommand := (*currentCommand).(lsCommand)

				currentLsCommandItems := &(currentLsCommand.items)
				name := tokens[1]
				*currentLsCommandItems = append(*currentLsCommandItems, folderItem{name: name})

				*currentCommand = currentLsCommand
			}
		} else if size, err := strconv.Atoi(tokens[0]); err == nil {
			if len(commands) == 0 {
				return commands, errors.New("output with no preceding command")
			}

			currentCommand := &commands[len(commands)-1]
			if (*currentCommand).commandType() == lsCommandType {
				currentLsCommand := (*currentCommand).(lsCommand)

				currentLsCommandItems := &(currentLsCommand.items)
				name := tokens[1]
				*currentLsCommandItems = append(*currentLsCommandItems, fileItem{name: name, size: size})

				*currentCommand = currentLsCommand
			}
		} else {
			return commands, errors.New(fmt.Sprintf("invalid terminal output: line starting with \"%s\" is invalid", tokens[0]))
		}
	}

	return commands, nil
}

func buildTree(commands []command) ([]*folderNode, error) {
	folderNodes := make([]*folderNode, 0)
	stack := make([]*folderNode, 0)
	for _, c := range commands {
		switch c := c.(type) {
		case cdCommand:
			if c.directory == "/" {
				newMap := make(map[string]node)
				rootFolderNode := folderNode{name: c.directory, children: newMap}
				stack = append(stack, &rootFolderNode)
				folderNodes = append(folderNodes, &rootFolderNode)
			} else {
				currentFolderNode := stack[len(stack)-1]
				childNode := ((*currentFolderNode).children)[c.directory]
				switch childNode := childNode.(type) {
				case *folderNode:
					stack = append(stack, childNode)
				}
			}
		case cdParentCommand:
			if len(stack) == 0 {
				return folderNodes, errors.New("cannot navigate to parent of root directory")
			} else {
				stack = stack[:len(stack)-1]
			}
		case lsCommand:
			currentFolderNode := stack[len(stack)-1]

			if currentFolderNode == nil {
				return folderNodes, errors.New("output with no preceding command")
			}

			for _, i := range c.items {
				switch i := i.(type) {
				case fileItem:
					newFileNode := fileNode{name: i.name, size: i.size}
					currentFolderNodeChildren := &(currentFolderNode.children)
					(*currentFolderNodeChildren)[newFileNode.name] = &newFileNode
				case folderItem:
					newmap := make(map[string]node)
					newFolderNode := folderNode{name: i.name, children: newmap}
					currentFolderNodeChildren := &(currentFolderNode.children)
					(*currentFolderNodeChildren)[newFolderNode.name] = &newFolderNode
					folderNodes = append(folderNodes, &newFolderNode)
				}
			}
		}
	}

	return folderNodes, nil
}

type folderNode struct {
	name     string
	children map[string]node
}

type fileNode struct {
	name string
	size int
}

type node interface {
	getSize() int
}

func (f folderNode) getSize() int {
	totalSize := 0
	for _, child := range f.children {
		totalSize += child.getSize()
	}
	return totalSize
}

func (f fileNode) getSize() int {
	return f.size
}
