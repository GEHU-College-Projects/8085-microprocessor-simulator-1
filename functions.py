# mov, mvi, lxi, lda, sta, lhld, shld, stax, xchg
# add, adi , sub, inr, dcr, inx, dcx, dad, sui
# cma, cmp
# jmp, jc, jnc, jz, jnz,
# set, out

from collections import defaultdict

registers = [0] * 8
memory = [0] * 65536
flags = [0] * 5
halt = False

register_values = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'H': 5, 'L': 6, 'M': 7}
flag_values = {'S': 0, 'Z': 1, 'AC': 2, 'P': 3, 'C': 4}


def convert_to_hex_print():
    temp_registers = registers.copy()
    for i in range(len(temp_registers)):
        if int(temp_registers[i]) > 99:
            temp_registers[i] = hex(int(temp_registers[i]))[2:].upper()
    # print value of registers
    print("A: " + str(temp_registers[0]) + " B: " + str(temp_registers[1]) + " C: " + str(temp_registers[2]) + " D: " + str(temp_registers[3]) + " E: " + str(temp_registers[4]) + " H: " + str(temp_registers[5]) + " L: " + str(temp_registers[6]) + " M: " + str(temp_registers[7]))

def get_hex_register_value(registers):
    temp_registers = registers.copy()
    for i in range(len(temp_registers)):
        if int(temp_registers[i]) > 99:
            temp_registers[i] = hex(int(temp_registers[i]))[2:].upper()
            # if carry generated the carry flag is set
            if temp_registers[i][0] == '1':
                flags[flag_values['C']] = 1
                temp_registers[i] = temp_registers[i][1:]
    # print value of registers
    return temp_registers



def count_bytes(instruction):
    opcode = instruction.upper().split()[0]
    if opcode == 'LXI':
        return 3
    elif opcode in ['STA', 'LDA', 'SHLD', 'LHLD', 'JMP', 'JC', 'JNC', 'JP', 'JM', 'JZ', 'JNZ']:
        return 3
    elif opcode in ['MOV', 'ADD', 'ADC', 'SUB', 'SBB', 'ANA', 'ORA', 'XRA', 'CMP', 'ADI', 'ACI', 'SUI', 'SBI', 'ANI',
                    'ORI', 'XRI', 'CPI', 'PUSH', 'POP', 'INR', 'DCR', 'INX', 'DCX']:
        return 1
    elif opcode in ['MVI', 'ADI', 'ACI', 'SUI', 'SBI', 'ANI', 'ORI', 'XRI', 'CPI', 'OUT']:
        return 2
    elif opcode == 'STAX':
        return 1
    elif opcode == 'XCHG':
        return 1
    else:
        return 0


def mov(data):
    if data['src_reg'] == 'M':
        address = str(registers[register_values['H']]) + str(registers[register_values['L']])
        registers[register_values[data['dest_reg']]] = memory[int(address)]
        return
    registers[register_values[data['dest_reg']]] = registers[register_values[data['src_reg']]]
def mvi(data):
    registers[register_values[data['dest_reg']]] = data['value']


def lxi(data):
    data['value'] = str(data['value'])
    data['value'] = [data['value'][:2], data['value'][2:]]
    if data['dest_reg'] == 'H':
        registers[register_values['H']] = data['value'][0]
        registers[register_values['L']] = data['value'][1]
    elif data['dest_reg'] == 'B':
        registers[register_values['B']] = data['value'][0]
        registers[register_values['C']] = data['value'][1]
    elif data['dest_reg'] == 'D':
        registers[register_values['D']] = data['value'][0]
        registers[register_values['E']] = data['value'][1]


def lda(data):
    registers[register_values['A']] = memory[data['address']]


def sta(data):
    memory[data['address']] = registers[register_values['A']]


def lhld(data):
    registers[register_values['L']] = memory[data['address']]
    registers[register_values['H']] = memory[data['address'] + 1]


def shld(data):
    memory[data['address']] = registers[register_values['L']]
    memory[data['address'] + 1] = registers[register_values['H']]


def stax(data):
    if data['dest_reg'] == 'B':
        memory[registers[register_values['B']] + registers[register_values['C']]] = registers[register_values['A']]
    elif data['dest_reg'] == 'D':
        memory[registers[register_values['D']] + registers[register_values['E']]] = registers[register_values['A']]


def xchg(data):
    registers[register_values['H']], registers[register_values['D']] = registers[register_values['D']], registers[
        register_values['H']]
    registers[register_values['L']], registers[register_values['E']] = registers[register_values['E']], registers[
        register_values['L']]


def add(data):
    registers[register_values['A']] = int(registers[register_values['A']]) + int(registers[register_values[data['dest_reg']]])


def adi(data):
    registers[register_values['A']] = int(registers[register_values['A']]) + int(data['value'])
    if registers[register_values['A']] > 255:
        registers[register_values['A']] -= 256
        flags[flag_values['C']] = 1


def sub(data):
    registers[register_values['A']] -= registers[register_values[data['src_reg']]]


def inr(data):
    registers[register_values[data['dest_reg']]] += 1


def dcr(data):
    registers[register_values[data['dest_reg']]] -= 1


def inx(data):
    if data['dest_reg'] == 'B':
        registers[register_values['C']] = int(registers[register_values['C']])+1
        if registers[register_values['C']] == 0:
            registers[register_values['B']] = int(registers[register_values['B']])+1
    elif data['dest_reg'] == 'D':
        registers[register_values['E']] = int(registers[register_values['E']])+1
        if registers[register_values['E']] == 0:
            registers[register_values['D']] = int(registers[register_values['D']])+1
    elif data['dest_reg'] == 'H':
        registers[register_values['L']] = int(registers[register_values['L']])+1
        if registers[register_values['L']] == 0:
            registers[register_values['H']] = int(registers[register_values['H']])+1


def dcx(data):
    if data['dest_reg'] == 'B':
        registers[register_values['C']] = int(registers[register_values['C']])-1
        if registers[register_values['C']] == 0:
            registers[register_values['B']] = int(registers[register_values['B']])-1
    elif data['dest_reg'] == 'D':
        registers[register_values['E']] = int(registers[register_values['E']])-1
        if registers[register_values['E']] == 0:
            registers[register_values['D']] = int(registers[register_values['D']])-1
    elif data['dest_reg'] == 'H':
        registers[register_values['L']] = int(registers[register_values['L']])-1
        if registers[register_values['L']] == 0:
            registers[register_values['H']] -= 1


def dad(data):
    if data['dest_reg'] == 'B':
        registers[register_values['C']] += registers[register_values['E']]
        if registers[register_values['C']] > 255:
            registers[register_values['C']] -= 256
            registers[register_values['B']] += 1
    elif data['dest_reg'] == 'D':
        registers[register_values['E']] += registers[register_values['L']]
        if registers[register_values['E']] > 255:
            registers[register_values['E']] -= 256
            registers[register_values['D']] += 1
    elif data['dest_reg'] == 'H':
        registers[register_values['L']] += registers[register_values['B']]
        if registers[register_values['L']] > 255:
            registers[register_values['L']] -= 256
            registers[register_values['H']] += 1


def sui(data):
    registers[register_values['A']] -= data['value']
    if registers[register_values['A']] < 0:
        registers[register_values['A']] += 256
        flags[flag_values['C']] = 1


def cmp(data):
    if registers[register_values['A']] == registers[register_values[data['src_reg']]]:
        flags[flag_values['Z']] = 1
    elif registers[register_values['A']] > registers[register_values[data['src_reg']]]:
        flags[flag_values['C']] = 1


def cma(data):
    if registers[register_values['A']] == data['value']:
        flags[flag_values['Z']] = 1
    elif registers[register_values['A']] > data['value']:
        flags[flag_values['C']] = 1


def out(data):
    print("OUT: ", data['address'], " - ",  memory[data['address']])



def set(data):
    print("SET: ", data['address'], data['value'])
    memory[int(data['address'])] = data['value']


