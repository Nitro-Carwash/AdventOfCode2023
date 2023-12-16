from enum import IntEnum


class Direction(IntEnum):
    North = 0,
    East = 1,
    South = 2,
    West = 3

    def direction_to_offset(self):
        match self:
            case Direction.North: return 0, -1
            case Direction.South: return 0, 1
            case Direction.West: return -1, 0
            case Direction.East: return 1, 0


def load_input():
    with open('in16', 'r') as in_stream:
        return [list(line.strip()) for line in in_stream.readlines()]


def calculate_energized_tiles(puzzle_input, start, start_direction):
    # seen = {(x, y) : {set(Direction)}}
    seen = {}
    dfs = [(start, start_direction)]

    while len(dfs) > 0:
        current_pos, direction = dfs.pop()
        x, y = current_pos
        if not (0 <= x < len(puzzle_input[0]) and 0 <= y < len(puzzle_input)):
            continue
        if current_pos not in seen:
            seen[current_pos] = set()
        if direction in seen[current_pos]:
            continue
        seen[current_pos].add(direction)

        if puzzle_input[y][x] == '-' and direction in [Direction.North, Direction.South]:
            dfs.append(((x + 1, y), Direction.East))
            dfs.append(((x - 1, y), Direction.West))
        elif puzzle_input[y][x] == '|' and direction not in [Direction.North, Direction.South]:
            dfs.append(((x, y + 1), Direction.South))
            dfs.append(((x, y - 1), Direction.North))
        else:
            if puzzle_input[y][x] == '\\':
                direction = Direction((direction - 1) % 4) if direction in [Direction.North, Direction.South] else Direction((direction + 1) % 4)
            elif puzzle_input[y][x] == '/':
                direction = Direction(direction + 1) if direction in [Direction.North, Direction.South] else Direction(direction - 1)

            offset = direction.direction_to_offset()
            dfs.append(((x + offset[0], y + offset[1]), direction))

    return len(seen)


def part2(puzzle_input):
    max_energize = 0
    for y in range(len(puzzle_input)):
        max_energize = max(max_energize, calculate_energized_tiles(puzzle_input, (0, y), Direction.East))
        max_energize = max(max_energize, calculate_energized_tiles(puzzle_input, (len(puzzle_input[0]) - 1, y), Direction.West))
    for x in range(len(puzzle_input[0])):
        max_energize = max(max_energize, calculate_energized_tiles(puzzle_input, (x, 0), Direction.South))
        max_energize = max(max_energize, calculate_energized_tiles(puzzle_input, (x, len(puzzle_input) - 1), Direction.North))
    return max_energize


print(f"Part 1:", calculate_energized_tiles(load_input(), (0, 0), Direction.East))
print(f"Part 2:", part2(load_input()))
