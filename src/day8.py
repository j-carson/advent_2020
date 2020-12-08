from dataclasses import dataclass, field
from collections import namedtuple


@dataclass
class Machine:
    iptr: int = 0
    value: int = 0
    code: list = field(default_factory=list)
    visited: set = field(default_factory=set)
    nopjmps: set = field(default_factory=set)

    def execute1(self):
        ins = self.code[self.iptr]

        if ins.opcode in ("nop", "jmp"):
            self.nopjmps.add(self.iptr)

        if ins.opcode == "jmp":
            self.iptr += ins.arg
        else:
            self.iptr += 1

        if ins.opcode == "acc":
            self.value += ins.arg

    def detect_loop(self):
        while self.iptr not in self.visited:
            self.visited.add(self.iptr)
            self.execute1()
        return self.value

    def attempt_repair(self):

        for iptr in self.nopjmps.copy():
            old_ins = self.code[iptr]
            new_ins = Instruction(
                "jmp" if old_ins.opcode == "nop" else "nop", old_ins.arg
            )

            self.code[iptr] = new_ins
            self.iptr = 0
            self.value = 0
            self.visited = set()
            self.nopjmps = set()

            try:
                self.detect_loop()
            except IndexError:
                # program ended - we're done
                return self.value
            else:
                # detected a loop, put this change back and try another
                self.code[iptr] = old_ins

        # fallback
        raise Exception("repair failed")


if __name__ == "__main__":
    # Read in the instructions
    code = []
    Instruction = namedtuple("Instruction", "opcode,arg")

    with open("code.txt") as fp:
        data = fp.read().splitlines()
    for ins in data:
        opcode, arg = ins.split()
        code.append(Instruction(opcode, int(arg)))

    # Create a simulator to run the instructions
    machine = Machine(0, 0, code)

    # Q1 - what is in the accumulator just before an instruction
    # runs for a second time?
    print(machine.detect_loop())

    # Q2 - what is in the accumulator just before code exit
    # on the repaired program?
    print(machine.attempt_repair())
