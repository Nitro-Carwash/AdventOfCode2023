def load_input():
    puzzle_input = []
    with open('in09', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def extrapolate_history(history):
    history_rows = [history]
    while len(set(history_rows[-1])) > 1:
        last_row = history_rows[-1]
        history_rows.append([last_row[i] - last_row[i - 1] for i in range(1, len(last_row))])

    [history_rows[i].append(history_rows[i][-1] + history_rows[i + 1][-1]) for i in reversed(range(len(history_rows) - 1))]
    return history_rows[0][-1]


def solve(puzzle_input):
    total = 0
    for line in puzzle_input:
        history = [int(entry) for entry in line.split(' ')]
        extrapolated = extrapolate_history(history)
        total += extrapolated
    return total


print(solve(load_input()))
