import re


def load_input():
    puzzle_input = []
    with open('in01', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    total = 0
    for line in puzzle_input:
        first_match = re.match(r".*?(\d)", line)
        last_match = re.match(r".*(\d)", line)
        total += 10 * int(first_match.group(1)) + int(last_match.group(1))
    return total


print(solve(load_input()))
