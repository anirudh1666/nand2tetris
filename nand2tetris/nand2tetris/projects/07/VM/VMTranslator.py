# This is the main driver program for the virtual machine in
# Hack.

from parser_2 import Parser
from code import Code
import sys
import os, os.path


def generate_code_dir(path, code):

    files = os.listdir(path)
    for file in files:
        generate_code(file, code)


def generate_code(file, code):

    parser = Parser(file)
    code.set_file_name(file[:file.index('.')])

    
    while parser.has_more_commands():
        parser.advance()
        command_t = parser.command_type()
        if command_t == 'C_ARITHMETIC':
            code.write_arithmetic(parser.arg1())
        elif command_t == 'C_PUSH':
            code.write_push_pop('push', parser.arg1(), int(parser.arg2()))
        elif command_t == 'C_POP':
            code.write_push_pop('pop', parser.arg1(), int(parser.arg2()))
        elif command_t == 'C_LABEL':
            code.write_label(parser.arg1())
        elif command_t == 'C_IF':
            code.write_if(parser.arg1())
        elif command_t == 'C_GOTO':
            code.write_goto(parser.arg1())

    parser.print()

# Run it by typing python VMTranslator.py filename.vm in cmd.
path = sys.argv[1]
if path.endswith('.vm'):
    # File is given as command line arg.
    code = Code(path[:path.index('.')] + '.asm')
    generate_code(path, code)
else:
    # Directory is given as command line arg.
    code = Code(path + '.asm')
    generate_code_dir(path, code)
code.close()
