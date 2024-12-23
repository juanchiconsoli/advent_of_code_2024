from typing import List

PROGRAM = [2, 4, 1, 2, 7, 5, 4, 5, 0, 3, 1, 7, 5, 5, 3, 0]

PROGRAM_BINARY = [
    0b010,
    0b100,
    0b001,
    0b010,
    0b111,
    0b101,
    0b100,
    0b101,
    0b000,
    0b011,
    0b001,
    0b111,
    0b101,
    0b101,
    0b011,
    0b000,
]


class ProgramExecutor:

    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
        self._output = []
        self._instruction_pointer = 0

    def execute_program(self, program: List[int]):

        while True:
            if self._instruction_pointer >= len(program):
                break

            opcode = PROGRAM[self._instruction_pointer]
            operand = PROGRAM[self._instruction_pointer + 1]

            self.execute_instruction(opcode, operand)

    def execute_instruction(self, opcode: int, operand: int):

        increase_pointer = True

        if opcode == 0:
            self._a = self._a // (2 ** self.get_combo(operand))
        elif opcode == 1:
            self._b = self._b ^ operand
        elif opcode == 2:
            self._b = self.get_combo(operand) % 8
        elif opcode == 3:
            if self._a != 0:
                self._instruction_pointer = operand
                increase_pointer = False
        elif opcode == 4:
            self._b = self._b ^ self._c
        elif opcode == 5:
            self._output.append(self.get_combo(operand) % 8)
        elif opcode == 6:
            self._b = self._a // (2 ** self.get_combo(operand))
        elif opcode == 7:
            self._c = self._a // (2 ** self.get_combo(operand))

        if increase_pointer:
            self._instruction_pointer += 2

    def get_output(self):
        return self._output

    def get_combo(self, x: int):
        if x in [0, 1, 2, 3]:
            return x
        if x == 4:
            return self._a
        if x == 5:
            return self._b
        if x == 6:
            return self._c
        return -1


def find(program, ans):
    if program == []:
        return ans
    for t in range(8):
        a = ans << 3 | t
        b = a % 8
        b = b ^ 2
        c = a >> b
        b = b ^ c
        b = b ^ 7
        if b % 8 == program[-1]:
            sub = find(program[:-1], a)
            if sub is None:
                continue
            return sub


if __name__ == "__main__":

    register_a = 22817223
    register_b = 0
    register_c = 0

    mapper = ProgramExecutor(register_a, register_b, register_c)

    mapper.execute_program(PROGRAM)

    output = mapper.get_output()

    print(",".join(map(str, output)))

    binary_output = [bin(x)[2:] for x in output]

    print(",".join(binary_output))

    print(find(PROGRAM, 0))
