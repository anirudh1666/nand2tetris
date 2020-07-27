from parser_2 import *
from code import *
from symbol_table import *
import sys



# Algorithm:
# 1) Open parser object, code object and output file writer.
# 2) Read input file using parser. Pass the mnemonic to output file writer.
# 3) Continue until you reach the end.


# Sets up the assembler by making a code, parser and filewriter object.
# @params = path to .asm file.
# @returns = (parser, code, filewriter)
def set_up(input_file):

    parser = Parser(input_file)
    code = Code()
    input_file = input_file[:input_file.index('.')]
    writer = open(input_file + '.hack', 'w')

    return (parser, code, writer)


def generate_code(input_file):

    parser, code, writer = set_up(input_file)

    while parser.has_more_commands():
        line = ''
        parser.advance()
        command_t = parser.command_type()

        if command_t == 'A_COMMAND':
            line += '0'
            binary = parser.symbol()
            line += binary + '\n'
            writer.write(line)

        elif command_t == 'C_COMMAND':
            line += '111'
            comp = code.comp(parser.comp())
            dest = code.dest(parser.dest())
            jump = code.jump(parser.jump())
            line = line + comp + dest + jump + '\n'
            writer.write(line)

        elif command_t == 'L_COMMAND':
            continue

        print(line)

    writer.close()
    

filename = sys.argv[1]
generate_code(filename)
    
