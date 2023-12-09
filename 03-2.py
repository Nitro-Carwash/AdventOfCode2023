import re


def load_input():
    puzzle_input = []
    with open('in03-2', 'r') as in_stream:
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
    for line in [top, middle, bottom]:
        if line is not None:
            for match in re.finditer(r"(\d+)", line):
                for span_i in range(1, len(match.regs)):
                    numbers.append((int(match.group(1)), match.regs[span_i][0], match.regs[span_i][1] - 1))

    gear_indices = []
    for match in re.finditer(r"\*", middle):
        for span_i in range(0, len(match.regs)):
            gear_indices.append(match.regs[span_i][0])

    for gear_index in gear_indices:
        adjacent_numbers = []
        for number in numbers:
            value = number[0]
            start = number[1]
            end = number[2]

            if start - 1 <= gear_index <= end + 1:
                adjacent_numbers.append(value)

        if len(adjacent_numbers) == 2:
            total += adjacent_numbers[0] * adjacent_numbers[1]

    return total


print(solve(load_input()))
