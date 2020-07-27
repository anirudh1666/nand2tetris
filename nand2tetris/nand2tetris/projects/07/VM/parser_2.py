# This program is part of the nand2tetris course. It involves building
# a virtual machine to generate Hack Assembly code.

class Parser:

    def __init__(self, input_file):

        self.file = open(input_file, 'r')
        self.pointer = ''
        self.commands_read = 0
        self.commands = []
        self.forward_pass()
        self.arithmetic_c = ['add', 'sub', 'neg', 'eq', 'gt',
                             'lt', 'and', 'or', 'not']
        self.segments = ['argument', 'local', 'static', 'constant',
                         'this', 'that', 'pointer', 'temp']
    
    def forward_pass(self):

        for line in self.file:
            # Remove all whitespace and comments.
            line = line.replace(' ','')
            line = line.replace('\n','')
            line = line.replace('\t','')
            if '//' in line:
                index = line.index('//')
                line = line[:index]

            if line == '':
                continue
            self.commands.append(line)

            
    def has_more_commands(self):

        return self.commands_read != len(self.commands)

    def advance(self):

        self.pointer = self.commands[self.commands_read]
        self.commands_read += 1

    def command_type(self):

        for command in self.arithmetic_c:
            if command == self.pointer:
                return 'C_ARITHMETIC'

        if 'push' in self.pointer:
            return 'C_PUSH'

        if 'pop' in self.pointer:
            return 'C_POP'


    def arg1(self):

        for command in self.arithmetic_c:
            if command in self.pointer:
                return self.pointer

        for segment in self.segments:
            if segment in self.pointer:
                return segment

    def arg2(self):

        ret = ''
        for char in self.pointer:
            if char.isnumeric():
                ret += char

        return ret
        
