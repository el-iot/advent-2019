import errors


class OpCodes:
    def __init__(self):

        self.lookup = {
            op.CODE: op
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
                ADJUSTRBASE,
            ]
        }

    def get(self, value):

        if value not in self.lookup:
            raise errors.UnknownOpcodeError(value)

        return self.lookup[value]()


class OpCode:

    INPUTS = 0
    OUTPUTS = 0
    PARAMETERS = 0
    WRITES = 0

    def __repr__(self):
        return f"<<{self.NAME}>>"


class ADD(OpCode):

    NAME = "ADD"
    CODE = 1
    PARAMETERS = 3
    WRITES = 1

    def execute(self, computer, inputs, v1, v2, v3):

        computer.program[v3] = int(v1) + int(v2)


class MULTIPLY(OpCode):

    NAME = "MULTIPLY"
    CODE = 2
    PARAMETERS = 3
    WRITES = 1

    def execute(self, computer, inputs, v1, v2, v3):

        print(v1, v2, v3)
        computer.program[v3] = int(v1) * int(v2)


class SAVE(OpCode):

    INPUTS = 1
    NAME = "SAVE"
    CODE = 3
    PARAMETERS = 1
    WRITES = 1

    def execute(self, computer, inputs, v1):
        """
        Save the value of the inputs[0] to the address in parameters[0]
        """
        computer.program[v1] = inputs[0]


class OUTPUT(OpCode):

    NAME = "OUTPUT"
    CODE = 4
    OUTPUTS = 1
    PARAMETERS = 1

    def execute(self, computer, inputs, v1):
        """
        Output the value of the parameters[0]
        """
        return v1


class JUMPIFTRUE(OpCode):
    """
    Opcode 5 is jump-if-true:
    if the first parameter is non-zero,
    it sets the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.
    """

    NAME = "JUMP-IF-TRUE"
    CODE = 5
    PARAMETERS = 2

    def execute(self, computer, inputs, v1, v2):
        if v1 != 0:
            computer.pointer = int(v2)


class JUMPIFFALSE(OpCode):
    """
    Opcode 6 is jump-if-false:
    if the first parameter is zero,
    it sets the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.
    """

    NAME = "JUMP-IF-FALSE"
    CODE = 6
    PARAMETERS = 2

    def execute(self, computer, inputs, v1, v2):
        if v1 == 0:
            computer.pointer = int(v2)


class LESSTHAN(OpCode):
    """
    Opcode 7 is less than:
    if the first parameter is less than the second parameter,
    it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.
    """

    NAME = "LESS-THAN"
    CODE = 7
    PARAMETERS = 3
    WRITES = 1

    def execute(self, computer, inputs, v1, v2, v3):
        computer.program[v3] = int(v1 < v2)


class EQUALS(OpCode):
    """
    Opcode 8 is equals:
    if the first parameter is equal to the second parameter,
    it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.
    """

    NAME = "EQUALS"
    CODE = 8
    PARAMETERS = 3
    WRITES = 1

    def execute(self, computer, inputs, v1, v2, v3):
        computer.program[v3] = int(v1 == v2)


class ADJUSTRBASE(OpCode):
    """
    Opcode 9 adjusts the relative base by the value of its only parameter.
    The relative base increases (or decreases, if the value is negative)
    by the value of the parameter.
    """

    NAME = "ADJUST-RELATIVE-BASE"
    CODE = 9
    PARAMETERS = 1
    WRITES = 1

    def execute(self, computer, inputs, v1):
        computer.relative_base += v1


class BREAK(OpCode):

    NAME = "BREAK"
    CODE = 99

    def execute(self, computer, inputs):
        """
        Halt the program
        """
        computer.finished = True
