import re


def load_input():
    puzzle_input = []
    with open('in04', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    total = 0
    for line in puzzle_input:
        groups = re.match(r"Card .*: (.*) \| (.*)", line)
        winning_numbers = set(list(filter(lambda x: len(x) > 0, groups.group(1).split(' '))))
        present_numbers = list(filter(lambda x: len(x) > 0, groups.group(2).split(' ')))
        matches = sum(1 for n in present_numbers if n in winning_numbers)
        if matches > 0:
            total += 1 << (matches - 1)
    return total


print(solve(load_input()))
