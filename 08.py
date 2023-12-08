import re


class WastelandNode:

    def __init__(self, symbol, left, right):
        self.symbol = symbol
        self.right = right
        self.left = left
        self.z_dist = 0
        self.next = None

    def set_next(self, route):
        cur = self
        depth = 0
        for direction in route:
            if cur.symbol == 'ZZZ':
                self.z_dist = len(route) - depth
            depth += 1

            if direction == 'L':
                cur = cur.left
            else:
                cur = cur.right

        self.next = cur

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

            if symbol == 'AAA':
                start = node

    for node in created_nodes.values():
        node.set_next(route)

    return start, route


def solve():
    start, route = load_input()
    if start.symbol == 'ZZZ':
        return 0

    steps = 1
    cur = start
    while cur.next.symbol != 'ZZZ':
        steps += 1
        cur = cur.next

    return (steps * len(route)) - cur.z_dist


print(solve())
