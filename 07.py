import re
from functools import cmp_to_key
from collections import Counter

card_ordering = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_to_score = {card: index for (index, card) in enumerate(card_ordering.__reversed__())}


def load_input():
    puzzle_input = []
    with open('in07', 'r') as in_stream:
        for line in in_stream.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def get_hand_type(hand):
    freq = Counter(hand)
    freq = sorted(freq.values(), reverse=True)
    if freq[0] == 5:
        return 7
    if freq[0] == 4:
        return 6
    if freq[0] == 3:
        return 5 if freq[1] == 2 else 4
    if freq[0] == 2:
        return 3 if freq[1] == 2 else 2

    return 1


def compare_hands(a, b):
    a, b = a[0], b[0]
    type_a, type_b = get_hand_type(a), get_hand_type(b)

    if type_a != type_b:
        return type_a - type_b

    for i in range(len(a)):
        if a[i] != b[i]:
            return card_to_score[a[i]] - card_to_score[b[i]]
    return 0


def solve(puzzle_input):
    rounds = []
    for line in puzzle_input:
        hand_and_bid = re.match(r"(.*) (\d*)", line)
        rounds.append((hand_and_bid.group(1), int(hand_and_bid.group(2))))
    rounds = sorted(rounds, key=cmp_to_key(compare_hands))

    return sum([(i + 1) * hand[1] for (i, hand) in enumerate(rounds)])


print(solve(load_input()))
