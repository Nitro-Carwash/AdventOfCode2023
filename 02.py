import re


def load_input():
    puzzle_input = []
    with open('in02', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    colors = ['red', 'green', 'blue']
    color_limits = [12, 13, 14]
    color_regexes = [re.compile(r"(\d+) " + color) for color in colors]
    total = 0
    game_id = 1
    for line in puzzle_input:
        game_sets = re.match(r"Game .*: (.*)", line)

        is_game_possible = True
        for game_set in game_sets.group(1).split('; '):
            if not is_game_possible:
                break

            for color_reveal in game_set.split(", "):
                if not is_game_possible:
                    break
                for i in range(len(colors)):
                    color_match = re.match(color_regexes[i], color_reveal)
                    if color_match is not None and int(color_match.group(1)) > color_limits[i]:
                        is_game_possible = False
                        break

        if is_game_possible:
            total += game_id

        game_id += 1

    return total


print(solve(load_input()))
