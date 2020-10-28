import itertools
import json

from computer.computer import Computer
from computer.feedback import FeedbackLoop


def get_program():

    with open("tests.json", "r") as file:
        tests = json.load(file)
    return tests["feedback"]


def test_loop():

    program = get_program()
    program = [int(x) for x in program.replace("\n", "").split(",")]
    largest = 0

    for order in itertools.permutations(range(5, 10)):

        loop = FeedbackLoop(
            size=5, machine=Computer, instructions=program, inputs=order
        )
        output = loop.run([0])
        largest = max(output, largest)

    assert 4931744 == largest
