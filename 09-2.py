def load_input():
    puzzle_input = []
    with open('in09-2', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def backstrapolate_history(history):
    history_rows = [history]
    while len(set(history_rows[-1])) > 1:
        last_row = history_rows[-1]
        history_rows.append([last_row[i] - last_row[i - 1] for i in range(1, len(last_row))])

    [history_rows[i].insert(0, history_rows[i][0] - history_rows[i + 1][0]) for i in reversed(range(len(history_rows) - 1))]
    return history_rows[0][0]


def solve(puzzle_input):
    total = 0
    for line in puzzle_input:
        history = [int(entry) for entry in line.split(' ')]
        extrapolated = backstrapolate_history(history)
        total += extrapolated
    return total


print(solve(load_input()))
