import re


def load_input():
    puzzle_input = []
    with open('in04-2', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    total = 0
    card_multipliers = [1 for _ in puzzle_input]
    card_index = 0

    for line in puzzle_input:
        groups = re.match(r"Card .*: (.*) \| (.*)", line)
        winning_numbers = set(list(filter(lambda x: len(x) > 0, groups.group(1).split(' '))))
        present_numbers = list(filter(lambda x: len(x) > 0, groups.group(2).split(' ')))
        matches = sum(1 for n in present_numbers if n in winning_numbers)
        for i in range(matches):
            next_card_index = i + card_index + 1
            if next_card_index >= len(card_multipliers):
                break
            card_multipliers[next_card_index] += card_multipliers[card_index]

        total += card_multipliers[card_index]
        card_index += 1
    return total


print(solve(load_input()))


# [1, 2, 4, 4, 2, 1, 1, 1, 1, 1, 1, 1]