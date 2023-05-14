# mov, mvi, lxi, lda, sta, lhld, shld, stax, xchg
# add, adi , sub, inr, dcr, inx, dcx, dad, sui
# cma, cmp
# jmp, jc, jnc, jz, jnz,
# set, out

from collections import OrderedDict

memory = OrderedDict()
flags = {'Z': 0, 'S': 0, 'P': 0, 'CY': 0, 'AC': 0}
registers = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'H': 0, 'L': 0}


def count_bytes(opcode):
    opcode = opcode.upper().split()[0]
    byte_counts = {'LXI': 3, 'STA': 3, 'LDA': 3, 'SHLD': 3, 'LHLD': 3, 'JMP': 3, 'JC': 3, 'JNC': 3, 'JP': 3, 'JM': 3,
                   'JZ': 3, 'JNZ': 3, 'MOV': 1, 'ADD': 1, 'ADC': 1, 'SUB': 1, 'SBB': 1, 'ANA': 1, 'ORA': 1, 'XRA': 1,
                   'CMP': 1, 'ADI': 2, 'ACI': 2, 'SUI': 2, 'SBI': 2, 'ANI': 2, 'ORI': 2, 'XRI': 2, 'CPI': 2, 'PUSH': 1,
                   'POP': 1, 'INR': 1, 'DCR': 1, 'INX': 1, 'DCX': 1, 'MVI': 2, 'OUT': 2, 'STAX': 1, 'XCHG': 1, 'DAD': 1, 'OUT':1}
    return byte_counts.get(opcode, 0)


def print_values():
    print()
    print()
    print(f"{'MEMORY':<10} {'VALUE':<6}")
    for address, value in memory.items():
        print(f"{address:<10} {value:<6}")
    print()

    print(f"{'FLAGS':<5} {'VALUE':<6}")
    for flag, value in flags.items():
        print(f"{flag:<5} {value:<6}")
    print()

    print(f"{'REGISTERS':<5} {'VALUE':<6}")
    for reg, value in registers.items():
        print(f"{reg:<5} {value:<6}")
    print()


# set flags where needed

def mov(data):
    if data['operand2'] == 'M':
        address = str(registers['H']) + str(registers['L'])
        registers[data['operand1']] = hex(int(memory[int(address)]))
    else:
        registers[data['operand1']] = registers[data['operand2']]


def mvi(data):
    print(data['value'])
    registers[data['operand1']] = data['value']


def lxi(data):
    registers[data['register1']] = str(data['address'])[:2]
    registers[data['register2']] = str(data['address'])[2:]


def lda(data):
    try:
        registers['A'] = memory[data['address']]
    except KeyError:
        print(f"Memory address {data['address']} not found")


def sta(data):
    memory[data['address']] = registers['A']


def lhld(data):
    try:
        registers['L'] = memory[data['address']]
        registers['H'] = memory[data['address'] + 1]

    except KeyError:
        print(f"Memory address {data['address']} not found")


def shld(data):
    memory[data['address']] = registers['L']
    memory[data['address'] + 1] = registers['H']


def stax(data):
    address = str(registers[data['register2']]) + str(registers[data['register1']])
    memory[int(address)] = registers['A']


def xchg(data):
    registers['H'], registers['D'] = registers['D'], registers['H']
    registers['L'], registers['E'] = registers['E'], registers['L']


def add(data):
    if data['operand1'] == 'M':
        address = str(registers['H']) + str(registers['L'])
        print(address)
        a = int(memory[int(address)]) + int(str(registers['A']), 16)
    else:
        a = int(str(registers['A']), 16) + int(registers[data['operand1']], 16)
    registers['A'] = hex(a)
    if a > 255:
        flags['CY'] = 1
        registers['A'] = hex(a - 256)


def adi(data):
    a = int(registers['A'], 16) + int(data['value'], 16)
    registers['A'] = hex(a)


def sub(data):
    a = int(registers['A'], 16) - int(registers[data['operand1']], 16)
    registers['A'] = hex(a)


def sui(data):
    a = int(registers['A'], 16) - int(data['value'], 16)
    registers['A'] = hex(a)


def inr(data):
    a = int(str(registers[data['operand1']]), 16) + 1
    registers[data['operand1']] = a


def dcr(data):
    a = int(str(registers[data['operand1']]), 16) - 1
    registers[data['operand1']] = a


def inx(data):
    x = str(int(registers[data['register2']]) + 1)
    registers[data['register2']] = '{:02d}'.format(int(x))
    # registers[data['register1']] = str(int(registers[data['register1']]) + 1)


def dcx(data):
    registers[data['register2']] = str(int(registers[data['register2']]) - 1)
    registers[data['register1']] = str(int(registers[data['register1']]) - 1)


def dad(data):
    registers['H'] = str(int(registers['H']) + int(registers[data['register1']]))
    registers['L'] = str(int(registers['L']) + int(registers[data['register2']]))
    if int(registers['L']) > 99:
        registers['H'] = str(int(registers['H']) + 1)
        registers['L'] = str(int(registers['L']))[1:]


def cma(data):
    registers['A'] = ~registers['A']


def cmp(data):
    if registers['A'] == registers[data['operand1']]:
        flags['Z'] = 1
    elif registers['A'] > registers[data['operand1']]:
        flags['S'] = 1
    else:
        flags['S'] = 0
        flags['Z'] = 0


def sui(data):
    registers['A'] -= data['value']


def set(data):
    memory[data['address']] = data['value']

def out(data):
    print("OUT: ", data['address'], memory[data['address']])

def jnz(data):
    return data['address']

def jnc(data):
    return data['address']

def jc(data):
    if flags['CY'] == 1:
        return data['address']


# mvi b, 05
# mvi d, 00
# lxi h, 1000
# mvi a 00
# add m
# jnc : 2014
# inr d
# inx h
# dcr b
# jnz : 2009
# sta 3000
# mov a, d
# sta 3001