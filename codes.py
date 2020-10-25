import re


class UnknownOpcodeError(Exception):
    """
    Raised when there is an unknown opcode
    """

    pass


class OpCodes:
    def __init__(self):

        self.lookup = {
            op.OPCODE: op
            for op in [
                SAVE,
                ADD,
                MULTIPLY,
                BREAK,
                OUTPUT,
                JUMPIFTRUE,
                JUMPIFFALSE,
                LESSTHAN,
                EQUALS,
            ]
        }

    def get(self, value):

        if value not in self.lookup:
            raise UnknownOpcodeError(value)

        return self.lookup[value]()


class OpCode:

    INPUTS = 0
    OUTPUTS = 0
    PARAMETERS = 0

    def __repr__(self):
        return f"<<{self.NAME}>>"


class SAVE(OpCode):

    OPCODE = 3
    INPUTS = 1
    PARAMETERS = 1
    NAME = "SAVE"

    def execute(self, computer, inputs, parameters, modes, **kwargs):
        """
        Save the value of the inputs[0] to the address in parameters[0]
        """
        d1 = computer.program[parameters[0]] if modes[0] else parameters[0]
        computer.program[d1] = inputs[0]


class ADD(OpCode):

    OPCODE = 1
    PARAMETERS = 3
    NAME = "ADD"

    def execute(self, computer, inputs, parameters, modes, **kwargs):

        v1 = computer.program[parameters[0]] if not modes[0] else parameters[0]
        v2 = computer.program[parameters[1]] if not modes[1] else parameters[1]
        computer.program[parameters[2]] = str(int(v1) + int(v2))


class MULTIPLY(OpCode):

    OPCODE = 2
    PARAMETERS = 3
    NAME = "MULTIPLY"

    def execute(self, computer, inputs, parameters, modes, **kwargs):

        v1 = computer.program[parameters[0]] if not modes[0] else parameters[0]
        v2 = computer.program[parameters[1]] if not modes[1] else parameters[1]
        computer.program[parameters[2]] = str(int(v1) * int(v2))


class BREAK(OpCode):

    OPCODE = 99
    NAME = "BREAK"

    def execute(self, computer, inputs, parameters, modes, **kwargs):
        """
        Halt the program
        """
        computer.finished = True


class OUTPUT(OpCode):

    OPCODE = 4
    OUTPUTS = 1
    PARAMETERS = 1
    NAME = "OUTPUT"

    def execute(self, computer, inputs, parameters, modes, **kwargs):
        """
        Output the value of the parameters[0]
        """
        assert len(parameters) == 1

        return parameters[0] if modes[0] else computer.program[parameters[0]]


class JUMPIFTRUE(OpCode):
    """
    Opcode 5 is jump-if-true:
    if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.
    """

    OPCODE = 5
    PARAMETERS = 2
    NAME = "JUMP-IF-TRUE"

    def execute(self, computer, inputs, parameters, modes, **kwargs):

        v1 = computer.program[parameters[0]] if not modes[0] else parameters[0]
        v2 = computer.program[parameters[1]] if not modes[1] else parameters[1]

        if v1 != 0:
            computer.pointer = int(v2)


class JUMPIFFALSE(OpCode):
    """
    Opcode 6 is jump-if-false:
    if the first parameter is zero, it sets the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.
    """

    OPCODE = 6
    PARAMETERS = 2
    NAME = "JUMP-IF-FALSE"

    def execute(self, computer, inputs, parameters, modes, **kwargs):

        v1 = computer.program[parameters[0]] if not modes[0] else parameters[0]
        v2 = computer.program[parameters[1]] if not modes[1] else parameters[1]

        if v1 == 0:
            computer.pointer = int(v2)


class LESSTHAN(OpCode):
    """
    Opcode 7 is less than:
    if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.
    """

    OPCODE = 7
    PARAMETERS = 3
    NAME = "LESS-THAN"

    def execute(self, computer, inputs, parameters, modes, **kwargs):


        v1 = computer.program[parameters[0]] if not modes[0] else parameters[0]
        v2 = computer.program[parameters[1]] if not modes[1] else parameters[1]
        v3 = parameters[2] if not modes[2] else computer.program[parameters[2]]

        computer.program[v3] = int(v1 < v2)


class EQUALS(OpCode):
    """
    Opcode 8 is equals:
    if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.
    """

    OPCODE = 8
    PARAMETERS = 3
    NAME = "EQUALS"

    def execute(self, computer, inputs, parameters, modes, **kwargs):

        v1 = computer.program[parameters[0]] if not modes[0] else parameters[0]
        v2 = computer.program[parameters[1]] if not modes[1] else parameters[1]
        v3 = parameters[2] if not modes[2] else computer.program[parameters[2]]

        computer.program[v3] = int(v1 == v2)
