

def load_input():
    with open('in14', 'r') as in_stream:
        return [list(line.strip()) for line in in_stream.readlines()]


def tilt_platform(platform):
    boulders_per_row = [0 for _ in range(len(platform))]
    stopping_point_per_col = [0 for _ in range(len(platform[0]))]
    for y in range(len(platform)):
        for x in range(len(platform[0])):
            if platform[y][x] == 'O':
                boulders_per_row[stopping_point_per_col[x]] += 1
                stopping_point_per_col[x] += 1
            if platform[y][x] == '#':
                stopping_point_per_col[x] = y + 1
    return sum((i + 1) * count for i, count in enumerate(reversed(boulders_per_row)))


def tilt_platform_spin(platform):
    stopping_point_per_col = [0 for _ in range(len(platform[0]))]
    # North
    for y in range(len(platform)):
        for x in range(len(platform[0])):
            if platform[y][x] == 'O':
                platform[y][x] = '.'
                platform[stopping_point_per_col[x]][x] = 'O'
                stopping_point_per_col[x] += 1
            if platform[y][x] == '#':
                stopping_point_per_col[x] = y + 1

    # West
    stopping_point_per_row = [0 for _ in range(len(platform))]
    for x in range(len(platform[0])):
        for y in range(len(platform)):
            if platform[y][x] == 'O':
                platform[y][x] = '.'
                platform[y][stopping_point_per_row[y]] = 'O'
                stopping_point_per_row[y] += 1
            if platform[y][x] == '#':
                stopping_point_per_row[y] = x + 1

    # South
    stopping_point_per_col = [len(platform) - 1 for _ in range(len(platform[0]))]
    for y in reversed(range(len(platform))):
        for x in range(len(platform[0])):
            if platform[y][x] == 'O':
                platform[y][x] = '.'
                platform[stopping_point_per_col[x]][x] = 'O'
                stopping_point_per_col[x] -= 1
            if platform[y][x] == '#':
                stopping_point_per_col[x] = y - 1

    # East
    stopping_point_per_row = [len(platform[0]) - 1 for _ in range(len(platform))]
    for x in reversed(range(len(platform[0]))):
        for y in range(len(platform)):
            if platform[y][x] == 'O':
                platform[y][x] = '.'
                platform[y][stopping_point_per_row[y]] = 'O'
                stopping_point_per_row[y] -= 1
            if platform[y][x] == '#':
                stopping_point_per_row[y] = x - 1

    return platform


def part2(platform):
    memo = {}
    step_to_load = {}
    for i in range(1000):
        platform = tilt_platform_spin(platform)
        hashable_puzzle = tuple(tuple(row) for row in platform)
        if hashable_puzzle in memo:
            print(f"Cycle detected in {i} starting at {memo[hashable_puzzle]}")
            cycle_depth = ((1000000000 - memo[hashable_puzzle]) % (i - memo[hashable_puzzle]))
            return step_to_load[memo[hashable_puzzle] + cycle_depth - 1]
        memo[hashable_puzzle] = i
        step_to_load[i] = sum((i + 1) * sum(1 if tile == 'O' else 0 for tile in row) for i, row in enumerate(reversed(platform)))


platform = load_input()
print(f"Part 1: {tilt_platform(platform)}")
print(f"Part 2: {part2(platform)}")



