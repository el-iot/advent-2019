import json
from itertools import permutations

import requests

from computer import Computer


def get_program():
    url = "https://adventofcode.com/2019/day/7/input"
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
    response = requests.get(url, cookies=cookies)
    return response.text


def run_in_order(order, program):

    outputs = [0]
    for o in order:
        comp = Computer(program.copy())
        outputs = comp.run_program([o] + outputs, early_stopping=True)

    return outputs


if __name__ == "__main__":

    program = get_program()
    program = [int(x) for x in program.replace("\n", "").split(",")]

    greatest = -1
    combination = []

    for order in permutations([0, 1, 2, 3, 4]):
        result = run_in_order(order, program)
        assert len(result) == 1
        result = int(result[0])
        if result > greatest:
            combination = order
            print("%s > %s" % (result, greatest))
            greatest = result

    print(combination)
