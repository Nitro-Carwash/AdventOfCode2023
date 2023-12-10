import datetime


class PipeMap:

    XAdjacentOffsets = [-1, 0, 1, 0]
    YAdjacentOffsets = [0, -1, 0, 1]

    def __init__(self, pipe_map, start):
        self.pipe_map = pipe_map
        self.y_size = len(pipe_map)
        self.x_size = len(pipe_map[0])
        self.start = start
        self.main_loop = self.mark_main_loop()
        self.cycles = 0
        self.time_start = datetime.datetime.now()

    def get_tiles_connected_to_start(self):
        connected = []
        for adjacent_tile in self.get_adjacent_tiles(self.start[0], self.start[1]):
            next_x, next_y = adjacent_tile
            connected_to_adjacent = self.get_connected_tiles(next_x, next_y)
            if self.start in connected_to_adjacent:
                connected.append((next_x, next_y))

        if len(connected) != 2:
            print('Incorrect number of connected pipes found for start tile.  Connected tiles were: ' + str(connected))

        return connected

    def mark_main_loop(self):
        tiles_connected_to_start = self.get_tiles_connected_to_start()

        bfs = tiles_connected_to_start
        seen = set()
        seen.add(self.start)
        seen.add(tiles_connected_to_start[0])
        seen.add(tiles_connected_to_start[1])

        while len(bfs) > 0:
            current_tile = bfs.pop(0)
            for tile in self.get_connected_tiles(current_tile[0], current_tile[1]):
                if tile not in seen:
                    bfs.append(tile)
                    seen.add(tile)

        return list(seen)

    def count_enclosed(self):
        zoom_map = [['.'] + list('.'.join(row)) + ['.'] for row in self.pipe_map]
        row_len = len(zoom_map[0])
        zoom_map = [zoom_map[(i - 1)//2] if i % 2 == 1 else ['.' for _ in range(row_len)] for i in range(2 * len(zoom_map) + 1)]

        # Fill zoomed sections
        for tile in self.main_loop:
            for connected in self.get_connected_tiles(tile[0], tile[1]):
                delta = (connected[0] - tile[0], connected[1] - tile[1])
                interior_tile = PipeMap.map_original_pos_to_zoom((tile[0], tile[1]))
                interior_tile = (interior_tile[0] + delta[0], interior_tile[1] + delta[1])
                # connected on x-axis
                if delta[0] != 0:
                    zoom_map[interior_tile[1]][interior_tile[0]] = '-'
                else:
                    zoom_map[interior_tile[1]][interior_tile[0]] = '|'

        start = ([(i, row.index('S')) for i, row in enumerate(zoom_map) if 'S' in row])[0]
        zoom_map_obj = PipeMap(zoom_map, start)
        interiors = set()
        outside = set()
        for tile in zoom_map_obj.main_loop:
            for adj in zoom_map_obj.get_adjacent_tiles(tile[0], tile[1]):
                if adj in zoom_map_obj.main_loop or adj in interiors:
                    continue
                interiors = interiors.union(set(zoom_map_obj.floodfill(adj, outside)))
        self.debug_print_map(zoom_map, interiors)
        return len([tile for tile in interiors if tile[0] % 2 == 1 and tile[1] % 2 == 1])

    def floodfill(self, start, outside):
        print(f"[{datetime.datetime.now() - self.time_start}] Flood {self.cycles}")
        self.cycles += 1

        bfs = [start]
        seen = set(bfs)
        interior = []
        while len(bfs) > 0:
            x, y = bfs.pop(0)
            if (x, y) in outside or y == 0 or y == len(self.pipe_map) - 1 or x == 0 or x == len(self.pipe_map[0]) - 1:
                [outside.add(t) for t in interior]
                return []

            interior.append((x, y))
            for adj in self.get_adjacent_tiles(x, y):
                if adj not in seen and adj not in self.main_loop:
                    bfs.append(adj)
                    seen.add(adj)

        return interior

    @staticmethod
    def debug_print_map(map, interiors):
        for interior in interiors:
            map[interior[1]][interior[0]] = 'I'

        with open('out10', 'w') as out_stream:
            for row in map:
                out_stream.write(str(''.join(row)) + '\n')

    @staticmethod
    def map_original_pos_to_zoom(tile):
        return 2*tile[0] + 1, 2*tile[1] + 1

    @staticmethod
    def map_zoom_to_original_pos(tile):
        return (tile[0] - 1) // 2, (tile[1] - 1) // 2

    def get_adjacent_tiles(self, x, y):
        adjacent = []
        for i in range(len(PipeMap.XAdjacentOffsets)):
            next_x, next_y = x + PipeMap.XAdjacentOffsets[i], y + PipeMap.YAdjacentOffsets[i]
            if self.is_in_bounds(next_x, next_y):
                adjacent.append((next_x, next_y))
        return adjacent

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

    def get_connected_offsets_for_pipe(self, pipe_symbol):
        match pipe_symbol:
            case 'S':
                connected = self.get_tiles_connected_to_start()
                return [(c[0] - self.start[0], c[1] - self.start[1]) for c in connected]
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
    return pipe_map.count_enclosed()


print(solve(load_input()))
