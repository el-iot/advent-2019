import json

from computer import Computer

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
HEIGHT = 100
WIDTH = 90
BLACK = 0
WHITE = 1


class PaintRobot(Computer):
    """
    Emergency Hull-Painting Robot
    """

    def __init__(self, *args, **kwargs):
        """
        Add x, y co-ordinates and a direction
        """
        super().__init__(*args, **kwargs)

        self.direction_idx = 0
        self.x = 0
        self.y = 0
        self.grid = [[BLACK for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.painted = []

    def move(self):
        """
        Move the robot
        """
        dx, dy = DIRECTIONS[self.direction_idx]
        self.x += dx
        self.y += dy

    def paint(self, colour):
        """
        Paint the floor beneath the robot
        """
        self.grid[self.y][self.x] = colour
        self.painted.append((self.x, self.y))

    def turn(self, direction):
        """
        Turn the robot 0 means it should turn left 90 degrees,
        and 1 means it should turn right 90 degrees.
        """
        self.direction_idx = (self.direction_idx + (1 if direction else -1)) % 4

    def read_next_instruction(self):
        """
        Read the next set of instructions and optionally prompt for input
        """
        opcode, modes = self.parse_opcode_at_pointer()
        parameters = []
        inputs = []

        if opcode.INPUTS:
            inputs = [self.grid[self.y][self.x]]

        for _ in range(opcode.PARAMETERS):
            parameters += [int(self.program[self.pointer])]
            self.pointer += 1

        return {
            "opcode": opcode,
            "parameters": parameters,
            "modes": modes,
            "inputs": inputs,
        }

    def run(self, *args):
        """
        Run the program
        """
        outputs = []

        while not self.finished:
            instructions = self.read_next_instruction()
            output = self.execute(**instructions)
            if output is not None:
                yield output

        return outputs

    def render_grid(self):
        print("\n".join("".join(" " if e else "■" for e in row) for row in self.grid))


with open("inputs.json", "r") as file:
    program = json.load(file)["painter"]

paint_robot = PaintRobot(program)
inputs = [WHITE]
runner = paint_robot.run(inputs)

while not paint_robot.finished:

    try:
        colour = next(runner)
        direction = next(runner)
    except StopIteration:
        paint_robot.render_grid()
        print(len(set(paint_robot.painted)))
        break

    paint_robot.paint(colour)
    paint_robot.turn(direction)
    paint_robot.move()
