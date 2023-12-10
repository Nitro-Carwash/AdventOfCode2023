

class PipeMap:

    XAdjacentOffsets = [-1, 0, 1, 0]
    YAdjacentOffsets = [0, -1, 0, 1]

    def __init__(self, pipe_map, start):
        self.pipe_map = pipe_map
        self.y_size = len(pipe_map)
        self.x_size = len(pipe_map[0])
        self.start = start

    def get_tiles_connected_to_start(self):
        connected = []
        for i in range(len(PipeMap.XAdjacentOffsets)):
            next_x, next_y = self.start[0] + PipeMap.XAdjacentOffsets[i], self.start[1] + PipeMap.YAdjacentOffsets[i]
            if self.is_in_bounds(next_x, next_y):
                connected_to_adjacent = self.get_connected_tiles(next_x, next_y)
                if self.start in connected_to_adjacent:
                    connected.append((next_x, next_y))

        if len(connected) != 2:
            print('Incorrect number of connected pipes found for start tile.  Connected tiles were: ' + str(connected))

        return connected

    def get_furthest_dist_from_start(self):
        tiles_connected_to_start = self.get_tiles_connected_to_start()

        # bfs tuple is ((x, y), depth)
        bfs = [(tile, 1) for tile in tiles_connected_to_start]
        seen = set(self.start)
        seen.add(tiles_connected_to_start[0])
        seen.add(tiles_connected_to_start[1])
        max_depth = 0

        while len(bfs) > 0:
            current_tile, current_depth = bfs.pop(0)
            max_depth = max(max_depth, current_depth)
            for tile in self.get_connected_tiles(current_tile[0], current_tile[1]):
                if tile not in seen:
                    bfs.append((tile, current_depth + 1))
                    seen.add(tile)
        return max_depth

    def get_connected_tiles(self, x, y):
        connected_tiles = []
        pipe_symbol = self.pipe_map[y][x]
        offsets = self.get_connected_offsets_for_pipe(pipe_symbol)
        if offsets is None:
            return []
        for offset in offsets:
            if self.is_in_bounds(x + offset[0], y + offset[1]):
                connected_tiles.append((x + offset[0], y + offset[1]))
        return connected_tiles

    def is_in_bounds(self, x, y):
        return 0 <= x < self.x_size and 0 <= y < self.y_size

    @staticmethod
    def get_connected_offsets_for_pipe(pipe_symbol):
        match pipe_symbol:
            case '|':
                return [(0, -1), (0, 1)]
            case '-':
                return [(-1, 0), (1, 0)]
            case 'L':
                return [(0, -1), (1, 0)]
            case 'J':
                return [(0, -1), (-1, 0)]
            case '7':
                return [(-1, 0), (0, 1)]
            case 'F':
                return [(1, 0), (0, 1)]
        return None


def load_input():
    puzzle_input = []
    with open('in10', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def solve(puzzle_input):
    pipe_map = []
    y = 0
    start = ()
    for line in puzzle_input:
        pipe_map.append([tile for tile in line])
        if 'S' in pipe_map[y]:
            start = (pipe_map[y].index('S'), y)
        y += 1

    pipe_map = PipeMap(pipe_map, start)
    return pipe_map.get_furthest_dist_from_start()


print(solve(load_input()))
