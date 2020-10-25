from codes import OpCodes


class Computer:
    """
    Computer
    """

    def __init__(self, program):

        if isinstance(program, str):
            program = [int(n) for n in program.replace("\n", "").split(",")]

        self.finished = False
        self.inputs = None
        self.opcodes = OpCodes()
        self.pointer = 0
        self.program = program

    def parse_opcode_at_pointer(self):
        """
        Parse an instruction underneath the pointer into an opcode and parameters
        and then advance the pointer
        """
        bits = [*str(self.program[self.pointer])]
        self.pointer += 1

        bits = [0] * (5 - len(bits)) + bits

        opcode_tail = bits.pop()
        opcode_head = bits.pop()
        opcode = int(str(opcode_head) + str(opcode_tail))

        modes = [int(e) for e in bits][::-1]

        return self.opcodes.get(opcode), modes

    def read_next_instruction(self):
        """
        Read the next set of instructions
        """
        opcode, modes = self.parse_opcode_at_pointer()
        parameters = []
        inputs = []

        if (n_inputs := opcode.INPUTS) > 0:
            assert len(self.inputs) == n_inputs
            inputs = self.inputs
            self.inputs = None

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
        return opcode.execute(self, parameters=parameters, modes=modes, inputs=inputs)

    def run_program(self, inputs=[]):
        """
        Run the program
        """
        self.inputs = inputs

        while not self.finished:
            instructions = self.read_next_instruction()
            output = self.execute(**instructions)
            print(">> %s" % output) if output is not None else None

        return output


if __name__ == "__main__":

    with open("instructions.txt", "r") as file:
        inst = [int(x) for x in file.read().replace("\n", "").split(",")]

    computer = Computer(inst)
    computer.run_program(inputs=[5])
