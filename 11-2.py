

class StarTile:
    def __init__(self, x, y, x_cost, y_cost, symbol):
        self.x = x
        self.y = y
        self.x_cost = x_cost
        self.y_cost = y_cost
        self.symbol = symbol


def load_input():
    puzzle_input = []
    with open('in11', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def inject_expansions(starmap, injection_size):
    # Inject columns
    for x in range(len(starmap[0])):
        if not any(tile.symbol == '#' for tile in [starmap[y][x] for y in range(len(starmap))]):
            for y in range(len(starmap)):
                starmap[y][x].x_cost = injection_size

    # Inject rows
    for y in range(len(starmap)):
        if not any(tile.symbol == '#' for tile in [starmap[y][x] for x in range(len(starmap[0]))]):
            for x in range(len(starmap[0])):
                starmap[y][x].y_cost = injection_size


def get_distance_between_galaxies(starmap, galaxy, other_galaxy):
    distance =  sum([tile.x_cost for tile in [starmap[galaxy.y][x] for x in range(min(galaxy.x, other_galaxy.x) + 1, max(galaxy.x, other_galaxy.x) + 1)]])
    distance += sum([tile.y_cost for tile in [starmap[y][galaxy.x] for y in range(min(galaxy.y, other_galaxy.y) + 1, max(galaxy.y, other_galaxy.y) + 1)]])

    return distance


def calculate_galaxy_distances(starmap):
    galaxies = []
    for y in range(len(starmap)):
        for x in range(len(starmap[0])):
            if starmap[y][x].symbol == '#':
                galaxies.append(starmap[y][x])

    total = 0
    seen = set()
    for galaxy in galaxies:
        seen.add(galaxy)
        for other_galaxy in galaxies:
            if other_galaxy in seen:
                continue
            total += get_distance_between_galaxies(starmap, galaxy, other_galaxy)

    return total


def solve(puzzle_input):
    starmap = []
    y = 0
    for line in puzzle_input:
        starmap.append([StarTile(i, y, 1, 1, tile) for (i, tile) in enumerate(line)])
        y += 1
        
    inject_expansions(starmap, 1000000)
    return calculate_galaxy_distances(starmap)


print(solve(load_input()))
