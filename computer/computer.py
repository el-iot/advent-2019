import errors
from codes import OpCodes
from modes import Modes


class Computer:
    """
    Computer
    """

    def __init__(self, program, memory=2048):

        if isinstance(program, str):
            program = [int(n) for n in program.replace("\n", "").split(",")]

        self.memory = memory
        self.program = program + [0] * (self.memory - len(program))

        self.finished = False
        self.inputs = []
        self.opcodes = OpCodes()
        self.pointer = 0
        self.relative_base = 0

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
                outputs.append(int(output))
                if early_stopping:
                    return outputs

        return outputs

    def read_next_instruction(self):
        """
        Read the next set of instructions
        """
        opcode, modes = self.parse_opcode_at_pointer()
        parameters = []
        inputs = []

        if opcode.INPUTS:
            inputs = [self.inputs.pop(0)]

        for _ in range(opcode.PARAMETERS):
            parameters += [int(self.program[self.pointer])]
            self.pointer += 1

        return {
            "opcode": opcode,
            "parameters": parameters,
            "modes": modes,
            "inputs": inputs,
        }

    def execute(self, opcode, parameters, modes, inputs):
        """
        Execute a set of instructions
        """

        values = []
        for mode, parameter in zip(modes, parameters):

            if mode == Modes.POSITION:
                # get the value at that position
                values.append(self.program[parameter])

            elif mode == Modes.IMMEDIATE:
                # use the raw value
                values.append(parameter)

            elif mode == Modes.RELATIVE:
                # use the relative position
                values.append(self.program[parameter + self.relative_base])

            else:
                raise errors.UnknownModeError(mode)

        if opcode.WRITES:
            values[-1] = (
                parameters[-1]
                if not modes[len(values) - 1]
                else self.relative_base + parameters[-1]
            )

        return opcode.execute(self, inputs, *values)

    def parse_opcode_at_pointer(self):
        """
        Parse an instruction underneath the pointer into an opcode and parameters
        and then advance the pointer
        """
        bits = [*str(self.program[self.pointer])]
        self.pointer += 1

        bits = [0] * (5 - len(bits)) + bits

        opcode = int("".join(map(str, bits[-2:])))
        modes = [int(e) for e in bits][2::-1]

        return self.opcodes.get(opcode), modes
