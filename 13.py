

def load_input():
    with open('in13', 'r') as in_stream:
        puzzle_input = [line.strip() for line in in_stream.readlines()]
        return [puzzle.split(',') for puzzle in ','.join([line for line in puzzle_input]).split(',,')]


def find_horizontal_reflections(pattern, smudges):
    reflect_candidates = [(i, smudges) for i in range(len(pattern) - 1)]
    for x in range(len(pattern[0])):
        remaining_reflect_candidates = []
        for candidate in reflect_candidates:
            y, smudges_remaining = candidate[0], candidate[1]
            offset = 0
            is_valid_reflect_spot = True
            while is_valid_reflect_spot:
                if y - offset < 0 or y + offset + 1 >= len(pattern):
                    break
                if pattern[y - offset][x] != pattern[y + offset + 1][x]:
                    smudges_remaining -= 1
                    if smudges_remaining == -1:
                        is_valid_reflect_spot = False
                offset += 1

            if is_valid_reflect_spot:
                remaining_reflect_candidates.append((y, smudges_remaining))
        reflect_candidates = remaining_reflect_candidates
    return sum(reflect_col[0] + 1 if reflect_col[1] == 0 else 0 for reflect_col in reflect_candidates)


def find_vertical_reflections(pattern, smudges):
    reflect_candidates = [(i, smudges) for i in range(len(pattern[0]) - 1)]
    for y in range(len(pattern)):
        remaining_reflect_candidates = []
        for candidate in reflect_candidates:
            x, smudges_remaining = candidate[0], candidate[1]
            offset = 0
            is_valid_reflect_spot = True
            while is_valid_reflect_spot:
                if x - offset < 0 or x + offset + 1 >= len(pattern[0]):
                    break
                if pattern[y][x - offset] != pattern[y][x + offset + 1]:
                    smudges_remaining -= 1
                    if smudges_remaining == -1:
                        is_valid_reflect_spot = False
                offset += 1

            if is_valid_reflect_spot:
                remaining_reflect_candidates.append((x, smudges_remaining))
        reflect_candidates = remaining_reflect_candidates
    return sum(reflect_col[0] + 1 if reflect_col[1] == 0 else 0 for reflect_col in reflect_candidates)


def solve(patterns, smudges):
    return sum(find_vertical_reflections(pattern, smudges) + 100 * find_horizontal_reflections(pattern, smudges) for pattern in patterns)


puzzle = load_input()
print(f"Part 1: {solve(puzzle, 0)}")
print(f"Part 2: {solve(puzzle, 1)}")
