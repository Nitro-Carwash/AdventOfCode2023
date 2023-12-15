def load_input():
    with open('in15', 'r') as in_stream:
        return in_stream.readlines()[0].split(',')


def run_hash(step):
    hash = 0
    for s in step:
        hash += ord(s)
        hash *= 17
        hash %= 256
    return hash


def insert_lenses(steps, boxes):
    for step in steps:
        if step[-1] == '-':
            operation = '-'
            label = step[:-1]
        else:
            focal_length = int(step[-1])
            operation = '='
            label = step[:-2]
        box_hash = run_hash(label)

        if operation == '=':
            if box_hash not in boxes:
                boxes[box_hash] = {}
            if label not in boxes[box_hash]:
                boxes[box_hash][label] = -1
            boxes[box_hash][label] = focal_length
        if operation == '-':
            if box_hash in boxes and label in boxes[box_hash]:
                boxes[box_hash].pop(label)

    return sum([sum([(box[0] + 1) * (i + 1) * focal for i, focal in enumerate(box[1].values())]) for box in boxes.items()])


boxes = {}
print(f"Part 1: {sum([run_hash(step) for step in load_input()])}")
print(f"Part 2: {insert_lenses(load_input(), boxes)}")
