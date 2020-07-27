# Parser class from nand2tetris. Used to build assembler.
from symbol_table import *

class Parser:

    def __init__(self, input_file):

        self.file = open(input_file)
        self.pointer = ''                    # Holds current command.
        self.commands_read = 0
        self.symbol_table = SymbolTable()
        self.avail_mem_location = 1024         # Start at RAM[1024]
        self.commands, self.symbol_table, self.avail_mem_location = forward_pass(self.file, self.symbol_table, self.avail_mem_location)

    # @returns = true if more commands to be read else false.
    def has_more_commands(self):

        return self.commands_read != len(self.commands)

    # Reads the next command in commands
    def advance(self):

        self.pointer = self.commands[self.commands_read]
        self.commands_read += 1

    # Forward pass removes L_COMMANDs so it should never be returned.
    # A_COMMANDS are commands of the format @xxx or @number
    # C_COMMANDs are of the form dest=comp;jump
    def command_type(self):

        if '@' in self.pointer:
            return 'A_COMMAND'

        if '(' in self.pointer:
            return 'L_COMMAND'

        return 'C_COMMAND'

    # Returns symbol mem location from symbol_table.
    # L_COMMANDs are removed so its called when you see A_COMMAND.
    # if @number then turn number into binary and return
    # @returns = mem address of symbol or binary representation of decimal number.
    def symbol(self):

        if self.symbol_table.contains(self.pointer[1:]):
            return self.symbol_table.get_address(self.pointer[1:])     # self.pointer[0] == '@'

        return format(int(self.pointer[1:]), 'b').zfill(15)
            
    # @returns = dest mnemonic. 
    def dest(self):

        ret = ''

        if '=' in self.pointer:
            index = self.pointer.index('=')
            ret = self.pointer[:index]

        return ret

    # @returns = the comp mnemonic
    def comp(self):

        ret = ''
        if '=' in self.pointer and ';' in self.pointer:
            index_eq = self.pointer.index('=')
            index_semi = self.pointer.index(';')
            ret = self.pointer[index_eq+1 : index_semi]

        elif '=' in self.pointer:
            index = self.pointer.index('=')
            ret = self.pointer[index + 1:]

        elif ';' in self.pointer:
            index = self.pointer.index(';')
            ret = self.pointer[:index]

        else:
            ret = self.pointer

        return ret

    # @returns = the jump mnemonic.
    def jump(self):

        if not ';' in self.pointer:
            return ''

        index = self.pointer.index(';')
        return self.pointer[index + 1:]


# Go through and delete all whitespaces and comments.
# Also count commands read and build symbol table.
# This is called when parser is initialized
# @params = file : file reader.
#           symbol_table : key = symbol, value = memory/instruction address
#           avail_mem_location : points to next available RAM memory address.
# @returns = all of params but updated.
def forward_pass(file, symbol_table, avail_mem_location):

    commands = []
    commands_read = 0                # Points to mem location. first line of translated code 
    for line in file:                # would go to RAM[0] etc. Helps with (xxx)
        # Remove all comments and whitespaces.
        line = line.replace(' ','')
        line = line.replace('\n','')
        line = line.replace('\t','')
        if '//' in line:
            index = line.index('//')
            line = line[:index]

        # Check if @ contains symbol. If it does add it to table.
        if '@' in line:
            index = line.index('@')
            if not line[index + 1:].isnumeric() and not symbol_table.contains(line[index + 1:]):
                symbol_table.add_entry(line[index + 1:], format(avail_mem_location, 'b').zfill(15))
                avail_mem_location += 1
                    
        if '(' in line:
            # From (xxx) add xxx to symbol table then continue. We don't need this line in commands.
            index_first = line.index('(')
            index_second = line.index(')')
            symbol_table.add_entry(line[index_first + 1: index_second], format(commands_read, 'b').zfill(15))
            continue

        if line == '':
            continue

        commands.append(line)
        commands_read += 1

    return (commands, symbol_table, avail_mem_location)


