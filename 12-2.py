import re

fold_count = 5


def load_input():
    puzzle_input = []
    with open('in12', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def get_possible_arrangements(record, sizes, start, memo, is_in_damaged=False, skip_writing_to_memo=False):
    if start >= len(record):
        return 1 if len(sizes) == 0 or (len(sizes) == 1 and sizes[0] == 0) else 0

    if start in memo:
        if sizes in memo[start]:
            return memo[start][sizes]

    arrangements = 0
    if record[start] == '#':
        if len(sizes) > 0 and sizes[0] > 0:
            next_sizes = list(sizes)
            next_sizes[0] -= 1
            arrangements = get_possible_arrangements(record, tuple(next_sizes), start + 1, memo, True)
    if record[start] == '.':
        if not is_in_damaged or (len(sizes) == 0 or sizes[0] == 0):
            if is_in_damaged and len(sizes) > 0:
                sizes = tuple(list(sizes)[1:])
            arrangements = get_possible_arrangements(record, sizes, start + 1, memo, False)
    if record[start] == '?':
        new_record = record.copy()
        new_record[start] = '.'
        # Skip memo because we don't want the '#' replacement to just return the lookup
        arrangements += get_possible_arrangements(new_record, sizes, start, memo, is_in_damaged, True)
        new_record[start] = '#'
        arrangements += get_possible_arrangements(new_record, sizes, start, memo, is_in_damaged, False)

    if not skip_writing_to_memo:
        if start not in memo:
            memo[start] = {}
        memo[start][sizes] = arrangements
    return arrangements


def solve(puzzle_input):
    total = 0
    for line in puzzle_input:
        line = re.match(r"(.+) (.+)", line)
        record = line.group(1)
        sizes = [int(size) for size in line.group(2).split(',')]
        record = list("?".join([record] * fold_count))
        sizes = tuple(sizes * fold_count)

        memo = {}
        total += get_possible_arrangements(record, sizes, 0, memo)
    return total


print(solve(load_input()))


