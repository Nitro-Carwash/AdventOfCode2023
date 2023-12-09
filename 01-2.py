import re

digit_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

digit_regex = re.compile(r"(\d)")


def load_input():
    puzzle_input = []
    with open('in01-2', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    total = 0

    regex_tuples = [(re.compile(r"(" + digit_words[i] + ")"), i) for i in range(len(digit_words))]

    for line in puzzle_input:
        first, last = get_digits_from_line(line, regex_tuples)
        total += 10 * first + last
    return total


def get_digits_from_line(line, regex_tuples):
    digits = []
    for regex_tuple in regex_tuples:
        for match in re.finditer(regex_tuple[0], line):
            for span_i in range(1, len(match.regs)):
                digits.append((match.regs[span_i][0], regex_tuple[1]))

    for match in re.finditer(digit_regex, line):
        for span_i in range(1, len(match.regs)):
            digits.append((match.regs[span_i][0], int(match.group(span_i))))

    if len(digits) == 0:
        print("found no digits in: " + line)
        return

    if len(digits) == 1:
        return digits[0][1], digits[0][1]

    digits = sorted(digits, key=lambda x: x[0])
    return digits[0][1], digits[-1][1]


print(solve(load_input()))
