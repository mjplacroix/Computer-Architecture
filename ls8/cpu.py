"""CPU functionality."""
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        self.ram = [0] * 256
        # self.reg = [R0, R1, R2, R3, R4, R5, R6, R7]
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        self.reg[self.SP] = 0xF4 
        self.FL = [0] * 8

    def load(self): 
        # """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     print(instruction)
        #     self.ram[address] = instruction
        #     address += 1
        # print(self.ram[:10])

        """ loading in program from the command line """
        filename = sys.argv[1]

        with open(filename) as f:
            address = 0
            for line in f:
                line = line.split('#')
                try:
                    v = int(line[0], 2)
                    # print(v)
                except ValueError:
                    continue

                self.ram[address] = v
                address += 1
            # print(self.ram[:10])

        
    def ram_read(self, address):
        """ ram_read() should accept the address to read and return the value stored there."""
        return self.ram[address]

    def ram_write(self, value, ram_id):
        """ ram_write() should accept a value to write, and the address to write it to."""
        self.ram[ram_id] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            # print(reg_a, reg_b)
            # print(self.reg[reg_a], self.reg[reg_b])
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            # print(f'CMP: {self.reg[reg_a], self.reg[reg_b]}')
            if self.reg[reg_a] == self.reg[reg_b]:
                # print('this_1')
                # set the 7th index [E] to 1
                self.FL[7] = 1
                # # no shift - increment E by 1
                # self.FL += 1
                # print(f'CMP[7] -> {self.FL}')
            elif self.reg[reg_a] < self.reg[reg_b]:
                # print('this_2')
                # set the 5th index to 1
                self.FL[5] = 1
                # self.FL = self.FL >> 2
                # # increment L in FLAG by 1
                # self.FL = 1
                # # shift FLAG left by 2
                # self.FL = self.FL << 2
            else:
                # print('this_3')
                # set the 6th index [G] to 1
                self.FL[6] = 1
                # # shift FLAG right by 1
                # self.FL = self.FL >> 1
                # # increment G in FLAG by 1
                # self.FL = 1
                # # shift FLAG left by 1
                # self.FL = self.FL << 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        ir = self.ram[self.pc]
        # print('1')

        HALT = 0b01
        LDI = 0b10000010
        PRN = 0b01000111
        NOP = 0b00000000
        MUL = 0b10100010
        CMP = 0b10100111
        PUSH = 0b01000101
        POP = 0b01000110
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        running = True

        while running:
            ir = self.ram[self.pc]
            if ir == HALT:
                running = False
            elif ir == LDI:
                operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
                # print(self.reg, operand_b)
                self.pc += 3
            elif ir == PRN:
                self.pc += 1
                print(self.reg[self.ram[self.pc]])
                self.pc += 1
            elif ir == NOP:
                self.pc += 1
            elif ir == MUL:
                self.pc += 1
                self.alu('MUL', self.ram[self.pc] , self.ram[self.pc + 1])
                # unsure if this should be adding 1 or 2
                self.pc += 2
            elif ir == CMP:
                self.pc += 1
                self.alu('CMP', self.ram[self.pc], self.ram[self.pc +1])
                self.pc += 2
            elif ir == PUSH:
                self.pc += 1
                self.reg[self.SP] -= 1

                # Copy the value in the given register to the address pointed to by SP.
                value = self.reg[self.ram[self.pc]]
                self.ram[self.reg[self.SP]] = value
                
                self.pc += 1
            elif ir == POP:
                self.pc += 1

                # Copy the value from the address pointed to by SP to the given register.
                value = self.ram[self.reg[self.SP]]
                self.reg[self.ram[self.pc]] = value                
                
                # Increment SP
                self.reg[self.SP] += 1
                self.pc += 1
            elif ir == JMP:
                
                # Jump to the address stored in the given register.
                new_address = self.reg[self.ram[self.pc + 1]]

                # Set the PC to the address stored in the given register.
                self.pc = new_address
            elif ir == JEQ:
                # if E on FLAG is true
                # # make a copy for manipulation then comparison
                # copyFL = self.FL
                # copyFL = copyFL << 7
                # copyFL = copyFL >> 7
                # if the 7th index is equal to 1
                if self.FL[7] == 1:
                    # go to registar entry for next pc
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += 2
            elif ir == JNE:
                # if E on FLAG is false
                # # make a copy for manipulation then comparison
                # copyFL_2 = self.FL
                # print(f'flag: {copyFL_2}')    # 0b00000000
                # copyFL_2 = copyFL_2 << 19
                # print(f'flag: {copyFL_2}')
                # copyFL_2 = copyFL_2 >> 8
                # print(f'flag: {copyFL_2}')
                # if copyFL_2 == 0:
                # print(f'FL-> {self.FL}')
                if self.FL[7] == 0:
                    # print(f'pc -> {self.pc}')
                    # go to registar entry for next pc
                    self.pc = self.reg[self.ram[self.pc + 1]]
                    # print(f'pc -> {self.pc}    ram -> {self.ram[self.pc]}')
                else:
                    self.pc += 2




                
