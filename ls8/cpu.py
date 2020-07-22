"""CPU functionality."""
import sys

# HALT = 0b01
# LDI = 0b10000010
# PRN = 0b01000111
# NOP = 0b00000000
# MUL = 0b10100010

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


        # ## branch table 
        # self.branchtable = {}
        # ## w/ each of the functions inserted
        # self.branchtable[HALT] = self.halt
        # self.branchtable[LDI] = self.ldi
        # self.branchtable[PRN] = self.prn
        # self.branchtable[NOP] = self.nop
        # self.branchtable[MUL] = self.mul


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
            print(self.reg)
            self.reg[reg_a] *= self.reg[reg_b]
            print(self.reg)
        elif op == 'CMP':
            pass
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
    
    ## new functions written for all 5 of these statements so far

    def halt(self):
        sys.exit()

    def ldi(self, pc):
        operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3
    
    def prn(self, pc):
        print(self.reg[self.pc])
        self.pc += 1

    def nop(self, pc):
        self.pc += 1
        pass

    def mul(self, pc):
        self.pc += 1
        self.alu('MUL', self.ram[self.pc] , self.ram[self.pc + 1])
        self.pc += 1



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

        # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
        # operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)


        # # self.branchtable[HALT]()
        # print('2')
        # self.branchtable[LDI](self.pc)
        # print('3')
        # self.branchtable[PRN](self.pc)
        # print('4')
        # self.branchtable[NOP](self.pc)
        # print('5')
        # self.branchtable[MUL](self.pc)
        # print('6')

        running = True

        while running:
            ir = self.ram[self.pc]
            if ir == HALT:
                running = False
            elif ir == LDI:
                operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
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


                
