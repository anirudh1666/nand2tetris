# This is the main driver program for the virtual machine in
# Hack.

from parser_2 import Parser
from code import Code
import sys
import os, os.path


def generate_code(path, code, directory):

    files = os.listdir(path)
    for file in files:
        generate_code(file, code)


def generate_code(file, code):

    parser = Parser(file)
    code.set_file_name(file[:file.index('.')] + '.asm')

    
    while parser.has_more_commands():
        parser.advance()
        command_t = parser.command_type()
        if command_t == 'C_ARITHMETIC':
            code.write_arithmetic(parser.arg1())
        elif command_t == 'C_PUSH':
            code.write_push_pop('push', parser.arg1(), int(parser.arg2()))
        elif command_t == 'C_POP':
            code.write_push_pop('pop', parser.arg1(), int(parser.arg2()))
    
    code.close()

code = Code()
path = sys.argv[1]
if path.endswith('.vm'):
    # File is given as command line arg.
    generate_code(path, code)
else:
    # Directory is given as command line arg.
    generate_code(path, code, True)
