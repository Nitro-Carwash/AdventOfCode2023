import re


def load_input():
    puzzle_input = []
    with open('in06', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    product = 1
    times = re.match(r"Time:\s+(.*)", puzzle_input[0]).group(1).split(' ')
    times = [int(time) for time in times if len(time) > 0]
    distances = re.match(r"Distance:\s+(.*)", puzzle_input[1]).group(1).split(' ')
    distances = [int(distance) for distance in distances if len(distance) > 0]

    for i in range(len(times)):
        time = times[i]
        record = distances[i]
        ways_to_beat = 0
        for t in range(1, time):
            if t * (time - t) > record:
                ways_to_beat += 1
        product *= ways_to_beat
    return product


print(solve(load_input()))
