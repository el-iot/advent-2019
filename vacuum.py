import json

from computer import Computer

DIRECTIONS = {
    "up": [(0, -1), "left", "right"],
    "down": [(0, 1), "right", "left"],
    "right": [(1, 0), "up", "down"],
    "left": [(-1, 0), "down", "up"],
}


class Vacuum(Computer):
    """
    Vacuum
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs, memory=2 ** 13)

        assert self.program[0] == 1
        self.program[0] = 2

        # start is at 18, 50
        self.x = 18
        self.y = 50
        self.direction = "up"
        self.outputs = []

    def get_inputs(self):
        """
        Get the inputs
        """
        return [self.inputs.pop(0)]

    def process_outputs(self, output):
        """
        Process outputs
        """
        self.outputs.append(output)

    def post_process(self):
        """
        Post Process
        """
        print(self.outputs)


def get_directions():
    """
    Get a set of movement instructions to traverse the scaffolding
    """
    with open("grid.txt", "r") as file:
        grid = file.read()

    DIRECTIONS = {
        "up": [(0, -1), "left", "right"],
        "down": [(0, 1), "right", "left"],
        "right": [(1, 0), "up", "down"],
        "left": [(-1, 0), "down", "up"],
    }

    grid = [[{".": 0, "#": 1}.get(e, 1) for e in x] for x in grid.split("\n") if x]
    x, y = 18, 50
    direction = "up"
    height = len(grid)
    width = len(grid[0])
    moves = []
    grid[y][x] = 2

    while any([i == 1 for j in grid for i in j]):

        assert grid[y][x] != 0

        grid[y][x] = 2

        (dx, dy), left, right = DIRECTIONS[direction]

        if 0 <= y + dy < height and 0 <= x + dx < width and grid[y + dy][x + dx] != 0:
            x += dx
            y += dy
            moves.append(direction)
            grid[y][x] = 2
            continue

        # we need to change direction

        for turn in [left, right]:
            (dx, dy), _, _ = DIRECTIONS[turn]
            if (
                0 <= y + dy < height
                and 0 <= x + dx < width
                and grid[y + dy][x + dx] != 0
            ):
                x += dx
                y += dy
                direction = turn
                moves.append(direction)
                grid[y][x] = 2
                break

    print("".join([move[0].upper() for move in moves]))


main_routine = ["B", "C", "B", "A", "C", "A", "C", "A", "B", "A"]

functions = {
    "A": ("R", 12, "L", 10, "R", 10, "L", 8),
    "B": ("R", 12, "L", 10, "R", 12),
    "C": ("L", 8, "R", 10, "R", 6),
}


def to_ascii(pattern):

    output = []
    separator = ord(",")
    terminator = ord("\n")

    for character in pattern:

        if isinstance(character, int):
            for digit in str(character):
                output.append(ord(digit))

        else:
            output.append(ord(character))

        output.append(separator)

    output.pop()
    output.append(terminator)

    return output


if __name__ == "__main__":

    with open("inputs.json", "r") as file:
        program = json.load(file)["scaffolding"]

    inputs = (
        to_ascii(main_routine)
        + sum([to_ascii(value) for key, value in sorted(functions.items())], [])
        + [ord("n"), ord("\n")]
    )

    vacuum = Vacuum(program)
    vacuum.inputs = inputs
    vacuum.run()
