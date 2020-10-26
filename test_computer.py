import json

from computer import Computer


def test_init():

    computer = Computer([0, 0, 0, 0])
    assert isinstance(computer, Computer)


def test_run():

    with open("tests.json", "r") as file:
        tests = json.load(file)

    for name, [program, inputs, expected] in tests['computer'].items():

        computer = Computer(program)
        outputs = computer.run(inputs=inputs)
        assert outputs == expected, name
