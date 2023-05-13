from functions import *


class Simulator:
    def __init__(self):
        self.pc = 0
        self.opcode = None
        self.dest_reg = None
        self.src_reg = None
        self.value = None
        self.address = None
        self.label = None
        self.function_dict = {
            'mov': mov,
            'mvi': mvi,
            'lxi': lxi,
            'lda': lda,
            'sta': sta,
            'lhld': lhld,
            'shld': shld,
            'stax': stax,
            'xchg': xchg,
            'add': add,
            'adi': adi,
            'sub': sub,
            'inr': inr,
            'dcr': dcr,
            'inx': inx,
            'dcx': dcx,
            'dad': dad,
            'sui': sui,
            'cma': cma,
            'cmp': cmp,
            'set': set,
            'out': out,
            # 'hlt': hlt,
        }

    def decode(self, instruction):
        parts = instruction.split()
        if len(parts) == 2:
            self.opcode = parts[0]
            second = parts[1]
            if len(second) == 1:
                self.dest_reg = second
            elif len(second) == 2:
                self.value = second
            elif len(second) == 4:
                self.address = second
        elif len(parts) == 3:
            self.opcode = parts[0]
            self.dest_reg = parts[1][:-1]
            self.src_reg_or_value = parts[2]
            if parts[1] == ":":
                self.opcode = parts[0]
                self.address = parts[2]
            elif len(self.dest_reg) == 4:
                self.address = self.dest_reg
                self.dest_reg = None
            elif self.src_reg_or_value.isdigit():
                self.value = int(self.src_reg_or_value)
            elif self.src_reg_or_value.startswith(":"):
                self.label = self.src_reg_or_value[1:]
            else:
                if len(self.src_reg_or_value) == 1:
                    self.src_reg = self.src_reg_or_value
                else:
                    self.value = self.src_reg_or_value
        elif len(parts) == 4:
            self.opcode = parts[0]
            self.dest_reg = parts[1]
            self.src_reg = parts[2]
            value_or_address = parts[3]
            if value_or_address.isdigit():
                self.value = int(value_or_address)
            else:
                self.address = value_or_address[1:]
        if self.value is not None:
            try:
                self.value = int(self.value)
            except:
                self.value = int(str(self.value), 16)
        if self.dest_reg is not None:
            print(self.dest_reg)
            # self.dest_reg = self.dest_reg[0]
        if self.address is not None:
            self.address = int(self.address)
        if self.dest_reg is not None:
            self.dest_reg = self.dest_reg.upper()
            if int(registers[register_values['C']]) != 0:
                flags[flag_values['Z']] = 0
            if int(registers[register_values['C']]-1 )== 0:
                flags[flag_values['Z']] = 1


        if self.src_reg is not None:
            self.src_reg = self.src_reg.upper()
        self.runCommand()

    def runCommand(self):
        data = {
            'opcode': self.opcode,
            'dest_reg': self.dest_reg,
            'src_reg': self.src_reg,
            'value': self.value,
            'address': self.address,
            'label': self.label,
            'pc': self.pc,
        }
        instruction = data['opcode'].lower()
        self.function_dict[instruction](data)

    def printState(self):
        convert_to_hex_print()
        print("Flags: ", flags)

    def storeCodeAtAddress(self, address):
        self.remove_empty_lines()
        initial_address = address
        with open('code.txt', 'r') as file:
            for instruction in file:
                opcode = instruction.split()[0]
                # print(opcode, count_bytes(instruction.upper()))
                memory[address] = instruction
                address += count_bytes(instruction.upper())
        self.execute(initial_address, last_address=address)

    def execute(self, address, last_address):
        print(address, last_address)
        while address < last_address:
            instruction = memory[int(address)]
            print(instruction, "inddddddd")
            opcode = instruction.split()[0]
            print(opcode)

            if opcode.upper() not in ['JMP', 'JC', 'JNC', 'JZ', 'JNZ']:
                self.decode(instruction)
                address += count_bytes(instruction)
            if flags[flag_values['Z']] == 1:
                print("Halting")
                self.printState()
                exit(0)
            elif opcode.upper() == "JNC" and flags[flag_values['C']] == 0:
                address = int(instruction.split()[2])
            elif opcode.upper() == "JNZ" and flags[flag_values['Z']] == 0:
                address = int(instruction.split()[2])
            elif opcode.upper() == "JC" and flags[flag_values['C']] == 1:
                address = int(instruction.split()[2])
            elif opcode.upper() == "JZ" and flags[flag_values['Z']] == 1:
                address = int(instruction.split()[2])
            elif opcode.upper() == "JMP":
                address = int(instruction.split()[1])
            elif opcode.upper() == "JNZ" and flags[flag_values['Z']] == 0:
                self.decode(instruction)
                address += count_bytes(instruction)
            # address += count_bytes(instruction)



    def set(self, address, data):
        memory[int(address)] = int(data)

    def setMemory(self):
        self.set(3000, 5)
        self.set(2050, 32)
        self.set(2051, 20)
        self.set(2052, 30)
        self.set(2053, 40)
        self.set(2054, 50)
        self.set(2055, 60)
        self.set(3051, 70)
        self.set(3052, 80)
        self.set(3053, 90)
        self.set(3054, 100)
        self.set(3055, 110)
        self.set(3056, 120)

    def saveTextToFile(self, text):
        with open('code.txt', 'w') as file:
            print(text)
            file.write(text)

    def get_text_from_file(self):
        with open('code.txt', 'r') as file:
            return file.read()

    def remove_empty_lines(self):
        lines=''
        with open('code.txt', 'r') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines if len(line.strip()) > 1]
        with open('code.txt', 'w') as file:
            for line in lines:
                file.write(line+'\n')
# main

if __name__ == '__main__':
    simulator = Simulator()
    simulator.setMemory()
    simulator.storeCodeAtAddress(2000)
    simulator.printState()
