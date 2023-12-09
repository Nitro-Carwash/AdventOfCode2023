import re
import numpy as np


def load_input():
    puzzle_input = []
    with open('in02-2', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    colors = ['red', 'green', 'blue']
    color_regexes = [re.compile(r"(\d+) " + color) for color in colors]
    total = 0

    for line in puzzle_input:
        game_sets = re.match(r"Game .*: (.*)", line)
        color_powers = [0, 0, 0]
        for game_set in game_sets.group(1).split('; '):
            for color_reveal in game_set.split(", "):
                for i in range(len(colors)):
                    color_match = re.match(color_regexes[i], color_reveal)
                    if color_match is not None:
                        color_powers[i] = max(color_powers[i], int(color_match.group(1)))
                        break

        total += np.prod(color_powers)

    return total


print(solve(load_input()))
