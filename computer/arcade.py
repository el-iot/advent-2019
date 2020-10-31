import json

import requests

from computer import Computer

HEIGHT = 30
WIDTH = 40


class Tiles:
    PADDLE = "P"
    BALL = "O"
    LOOKUP = {0: " ", 1: "W", 2: "B", 3: "P", 4: "O"}


class Arcade(Computer):
    def __init__(self, height, width, *args, **kwargs):
        super().__init__(*args, memory=4096, **kwargs)
        self.width = width
        self.height = height
        self.grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.score = None

    def run(self, inputs=[], early_stopping=False):
        """
        Run the program
        """
        self.inputs += inputs
        outputs = []

        while not self.finished:

            instructions = self.read_next_instruction()
            output = self.execute(**instructions)

            if output is not None:
                outputs.append(output)
                if len(outputs) == 3:
                    self.process_outputs(*outputs)
                    outputs = []

    def process_outputs(self, x, y, tile):
        """
        Process outputs
        """
        if x == -1 and y == 0:
            self.score = tile
            return

        self.grid[y][x] = Tiles.LOOKUP[tile]

    def read_next_instruction(self):
        """
        Read the next set of instructions
        """
        opcode, modes = self.parse_opcode_at_pointer()
        parameters = []
        inputs = []

        if opcode.INPUTS:
            inputs = [self.get_ball_direction()]

        for _ in range(opcode.PARAMETERS):
            parameters += [int(self.program[self.pointer])]
            self.pointer += 1

        return {
            "opcode": opcode,
            "parameters": parameters,
            "modes": modes,
            "inputs": inputs,
        }

    def get_ball_direction(self):

        px = [
            x
            for x in range(self.width)
            for y in range(self.height)
            if self.grid[y][x] == Tiles.PADDLE
        ][0]

        bx = [
            x
            for x in range(self.width)
            for y in range(self.height)
            if self.grid[y][x] == Tiles.BALL
        ][0]

        return -1 if px > bx else 0 if px == bx else 1


if __name__ == "__main__":

    url = "https://adventofcode.com/2019/day/13/input"
    with open("../cookies.json", "r") as file:
        cookies = json.load(file)

    response = requests.get(url, cookies=cookies)
    program = [int(x) for x in response.text.split(",")]
    program[0] = 2  # change the value at address 0

    arcade = Arcade(40, 40, program)
    arcade.run()

    print('FINAL SCORE: %s' % arcade.score)
