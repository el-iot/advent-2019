import itertools
import json

import requests

from .computer import Computer


class FeedbackLoop:
    """
    Feedback Loop of Machines
    """

    def __init__(self, size, machine, instructions, inputs):
        self.machines = [machine([x for x in instructions.copy()]) for _ in range(size)]
        self.inputs = inputs

    def run(self, initial_input):
        """
        Run the machines
        """
        idx = 0
        outputs = initial_input
        stack = []

        while not all(machine.finished for machine in self.machines):

            if outputs:
                stack += outputs

            machine = self.machines[idx % 5]
            inputs = [self.inputs[idx % 5]] if idx < 5 else []

            outputs = machine.run(inputs=inputs + outputs, early_stopping=True)
            idx += 1

        return stack[-1]


def get_program():

    url = "https://adventofcode.com/2019/day/7/input"
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
    response = requests.get(url, cookies=cookies)
    return response.text


if __name__ == "__main__":

    program = get_program()
    program = [int(x) for x in program.replace("\n", "").split(",")]
    largest = 0

    for order in itertools.permutations(range(5, 10)):

        loop = FeedbackLoop(
            size=5, machine=Computer, instructions=program, inputs=order
        )
        output = loop.run([0])
        largest = max(output, largest)

    print(f'found: {largest}')
