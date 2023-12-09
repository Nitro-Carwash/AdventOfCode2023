import re


def load_input():
    puzzle_input = []
    with open('in06-2', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    times = re.match(r"Time:\s+(.*)", puzzle_input[0]).group(1).split(' ')
    time = int(''.join(times))
    distances = re.match(r"Distance:\s+(.*)", puzzle_input[1]).group(1).split(' ')
    distance = int(''.join(distances))

    ways_to_beat = 0
    for t in range(1, time):
        if t * (time - t) > distance:
            ways_to_beat += 1
    return ways_to_beat


print(solve(load_input()))
