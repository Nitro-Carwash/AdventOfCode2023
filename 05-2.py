import re


def load_input():
    puzzle_input = []
    with open('in05-2', 'r') as in_stream:
        for line in in_stream.readlines():
            if line != '\n':
                puzzle_input.append(line.strip())

    return puzzle_input


def get_overlapping_ranges_with(range, existing_ranges):
    overlapping = []
    for partition in existing_ranges:
        if partition[0] > range[1]:
            break
        if partition[1] < range[0]:
            continue

        overlapping.append(partition)

    return overlapping


def merge_ranges(ranges):
    merged = []
    ranges = sorted(ranges, key=lambda x: x[0])
    merged.append(ranges[0])

    for range in ranges[1:]:
        latest = merged[-1]
        if latest[0] <= range[0] <= latest[1]:
            latest = (latest[0], max(latest[1], range[1]))
            merged.pop()
            merged.append(latest)
        else:
            merged.append(range)
    return merged


def merge_mappings_with_ranges(existing_ranges, mappings):
    mapping_results = []

    for mapping in mappings:
        overlapping = get_overlapping_ranges_with(mapping, existing_ranges)
        if len(overlapping) == 0:
            continue

        # Remove these from existing ranges
        [existing_ranges.remove(overlap) for overlap in overlapping]
        # Apply mapping to all overlapped and get resultant ranges, along with unchanged ranges
        unchanged, new = apply_mapping_to_ranges(overlapping, mapping)
        # replace unchanged ranges, and store mapping results
        existing_ranges.extend(unchanged)
        mapping_results.extend(new)

    mapping_results.extend(existing_ranges)
    # There shouldn't actually be any overlapping regions at this point according to my understanding, but
    # this should resolve any mapping mishaps
    mapping_results = merge_ranges(mapping_results)
    return mapping_results


def apply_mapping_to_ranges(ranges, mapping):
    unchanged_ranges = []
    new_ranges = []
    offset = mapping[2]

    for range in ranges:
        # Completely enveloped by new range
        if mapping[0] <= range[0] and range[1] <= mapping[1]:
            new_ranges.append((range[0] + offset, range[1] + offset))
        # Completely inside
        elif range[0] < mapping[0] and mapping[1] < range[1]:
            unchanged_ranges.append((range[0], mapping[0] - 1))
            new_ranges.append((mapping[0] + offset, mapping[1] + offset))
            unchanged_ranges.append((mapping[1] + 1, range[1]))
        # Partial overlap
        else:
            # Left overlap
            if mapping[1] < range[1]:
                # Split
                unchanged_ranges.append((mapping[1] + 1, range[1]))
                new_ranges.append((range[0] + offset, mapping[1] + offset))
            else:  # Right overlap
                # Shrink
                unchanged_ranges.append((range[0], mapping[0] - 1))
                new_ranges.append((mapping[0] + offset, range[1] + offset))

    return unchanged_ranges, new_ranges


def solve(puzzle_input):
    seeds = re.match(r"seeds: (.*)", puzzle_input[0]).group(1)
    seeds = [int(seed) for seed in seeds.split(' ')]
    seeds = [(seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)]
    ranges = sorted(seeds, key=lambda x: x[0])

    i = 2
    while i < len(puzzle_input):
        mappings = []
        while i < len(puzzle_input) and puzzle_input[i][0].isnumeric():
            map_row = puzzle_input[i].split(' ')
            destination = int(map_row[0])
            source = int(map_row[1])
            span = int(map_row[2])
            diff = destination - source
            mappings.append((source, source + span - 1, diff))

            i += 1
        mappings = sorted(mappings, key=lambda x: x[0])
        ranges = merge_mappings_with_ranges(ranges, mappings)
        i += 1

    return min(x[0] for x in ranges)


print(solve(load_input()))
