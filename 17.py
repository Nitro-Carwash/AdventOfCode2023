import heapq
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
    with open('in17', 'r') as in_stream:
        return [[int(c) for c in line.strip()] for line in in_stream.readlines()]


# Technically dijkstra but it ended up getting simplified by the fact that we encode the direction, so
# now it looks more like a greedy-first search
def dijkstra(city, start, end, part1):
    # heat, x, y, direction, duration
    heap = [(0, start[0], start[1], Direction.South, 0), (0, start[0], start[1], Direction.East, 0)]
    seen = set()
    while len(heap) > 0:
        p = heapq.heappop(heap)
        if p[1:] in seen:
            continue
        seen.add(p[1:])
        heat, x, y, direction, duration = p
        if (x, y) == end and (part1 or duration >= 4):
            return heat

        available_directions = [Direction((direction + 1) % 4), Direction((direction - 1) % 4)] if duration >= 4 or part1 else []
        if (duration < 3 and part1) or (duration < 10 and not part1):
            available_directions.append(direction)

        for next_direction in available_directions:
            offset = next_direction.direction_to_offset()
            next_x, next_y = x + offset[0], y + offset[1]
            if 0 <= next_x < len(city[0]) and 0 <= next_y < len(city):
                heapq.heappush(heap, (city[next_y][next_x] + heat, next_x, next_y, next_direction, 1 + duration if next_direction == direction else 1))


city_map = load_input()
print(f"part1: {dijkstra(city_map, (0, 0), (len(city_map[0])-1, len(city_map)-1), True)}")
print(f"part2: {dijkstra(city_map, (0, 0), (len(city_map[0])-1, len(city_map)-1), False)}")
