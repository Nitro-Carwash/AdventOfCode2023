import re


def load_input():
    puzzle_input = []
    with open('in03', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    top = None
    middle = puzzle_input[0]
    bottom = puzzle_input[1]
    total = solve_lines(top, middle, bottom)

    for line in puzzle_input[2:]:
        top = middle
        middle = bottom
        bottom = line

        total += solve_lines(top, middle, bottom)

    total += solve_lines(puzzle_input[-2], puzzle_input[-1], None)

    return total


def solve_lines(top, middle, bottom):
    total = 0
    numbers = []
    for match in re.finditer(r"(\d+)", middle):
        for span_i in range(1, len(match.regs)):
            numbers.append((int(match.group(1)), match.regs[span_i][0], match.regs[span_i][1] - 1))

    part_indices = set()
    for line in [top, middle, bottom]:
        if line is not None:
            for match in re.finditer(r"[^\d^.]", line):
                for span_i in range(0, len(match.regs)):
                    part_indices.add(match.regs[span_i][0])

    for part_index in part_indices:
        for number in numbers:
            value = number[0]
            start = number[1]
            end = number[2]

            if start - 1 <= part_index <= end + 1:
                total += value

    return total


print(solve(load_input()))
