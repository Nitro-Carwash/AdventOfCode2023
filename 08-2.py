import re
import itertools
from functools import reduce


class WastelandNode:
    def __init__(self, symbol, left, right):
        self.symbol = symbol
        self.right = right
        self.left = left
        self.z_distances = {}

    def find_z_distances(self, route):
        cur = self
        depth = 0
        seen = set()
        cycle_detected = False

        while not cycle_detected:
            if cur.symbol in seen:
                break
            seen.add(cur.symbol)

            for direction in route:
                if cur.symbol.endswith('Z') and cur.symbol not in self.z_distances:
                    self.z_distances[cur.symbol] = depth

                depth += 1

                if direction == 'L':
                    cur = cur.left
                else:
                    cur = cur.right

    def add_child(self, child):
        if self.left == child.symbol:
            self.left = child
        elif self.right == child.symbol:
            self.right = child
        else:
            print("not a matching child!")


def load_input():
    created_nodes = {}
    missing_nodes = {}
    starts = []
    ends = []

    with open('in08', 'r') as input:
        route = input.readline().strip()
        for line in input:
            if line == '\n':
                continue

            node_line = re.match(r"(.*) = \((.*), (.*)\)", line)
            symbol = node_line.group(1)
            left = node_line.group(2)
            right = node_line.group(3)

            node = WastelandNode(symbol, left, right)
            created_nodes[symbol] = node

            if left in created_nodes:
                node.left = created_nodes[left]
            else:
                if left not in missing_nodes:
                    missing_nodes[left] = []
                missing_nodes[left].append(node)

            if right in created_nodes:
                node.right = created_nodes[right]
            else:
                if right not in missing_nodes:
                    missing_nodes[right] = []
                missing_nodes[right].append(node)

            if symbol in missing_nodes:
                for missing_node in missing_nodes[symbol]:
                    missing_node.add_child(node)

            if symbol.endswith('A'):
                starts.append(node)
            if symbol.endswith('Z'):
                ends.append(node)

    for node in starts:
        node.find_z_distances(route)

    return starts, ends, route


def solve():
    starts, ends, route = load_input()
    c = []
    for element in itertools.product(*[start.z_distances.values() for start in starts]):
        c.append(element)

    return min(reduce(lcm, list(paths)) for paths in c)


def lcm(a, b):
    return a * int(b / gcd(a, b))


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


print(solve())
