

def load_input():
    with open('in14', 'r') as in_stream:
        return [list(line.strip()) for line in in_stream.readlines()]


def tilt_platform(platform, outer_range, inner_range, transform_to_coords):
    stopping_points = [outer_range.start for _ in inner_range]
    step = outer_range.step
    for i in outer_range:
        for j in inner_range:
            x, y = transform_to_coords(i, j)
            if platform[y][x] == 'O':
                platform[y][x] = '.'
                stop_x, stop_y = transform_to_coords(stopping_points[j], j)
                platform[stop_y][stop_x] = 'O'
                stopping_points[j] += step
            if platform[y][x] == '#':
                stopping_points[j] = i + step
    return platform


def tilt_platform_north(platform):
    return tilt_platform(platform, range(len(platform)), range(len(platform[0])), lambda i, j: (j, i))


def tilt_platform_south(platform):
    return tilt_platform(platform, range(len(platform))[::-1], range(len(platform[0])), lambda i, j: (j, i))


def tilt_platform_west(platform):
    return tilt_platform(platform, range(len(platform[0])), range(len(platform)), lambda i, j: (i, j))


def tilt_platform_east(platform):
    return tilt_platform(platform, range(len(platform[0]))[::-1], range(len(platform)), lambda i, j: (i, j))


def tilt_platform_spin(platform):
    platform = tilt_platform_north(platform)
    platform = tilt_platform_west(platform)
    platform = tilt_platform_south(platform)
    return tilt_platform_east(platform)


def score_platform_load(platform):
    return sum((i + 1) * sum(1 if tile == 'O' else 0 for tile in row) for i, row in enumerate(reversed(platform)))


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
        step_to_load[i] = score_platform_load(platform)


platform = load_input()
print(f"Part 1: {score_platform_load(tilt_platform_north(platform))}")
print(f"Part 2: {part2(platform)}")



