import re


def load_input():
    puzzle_input = []
    with open('in05', 'r') as in_stream:
        for line in in_stream.readlines():
            if line != '\n':
                puzzle_input.append(line.strip())

    return puzzle_input


def map_to_next_value(in_value, ranges):
    for range in ranges:
        if range[0] > in_value:
            break
        if range[0] <= in_value <= range[1]:
            return in_value + range[2]

    return in_value


def solve(puzzle_input):
    seeds = re.match(r"seeds: (.*)", puzzle_input[0]).group(1)
    seeds = [int(seed) for seed in seeds.split(' ')]

    i = 2
    while i < len(puzzle_input):
        ranges = []
        while i < len(puzzle_input) and puzzle_input[i][0].isnumeric():
            map_row = puzzle_input[i].split(' ')
            destination = int(map_row[0])
            source = int(map_row[1])
            span = int(map_row[2])
            diff = destination - source
            ranges.append((source, source + span - 1, diff))

            i += 1
        ranges = sorted(ranges, key=lambda x: x[0])
        seeds = [map_to_next_value(seed, ranges) for seed in seeds]
        i += 1

    return min(seeds)


print(solve(load_input()))
