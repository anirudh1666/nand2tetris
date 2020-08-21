# This program is part of the nand2tetris course. It involves building
# a virtual machine to generate Hack Assembly code.

class Parser:

    def __init__(self, input_file):

        self.file = open(input_file, 'r')
        self.pointer = ''
        self.commands_read = 0
        self.commands = []
        self.current_func = ['null']                                 # Behaves as a stack.
        self.labels = []
        self.functions = []
        self.forward_pass()
        self.second_pass()
        self.arithmetic_c = ['add', 'sub', 'neg', 'eq', 'gt',
                             'lt', 'and', 'or', 'not']
        self.segments = ['argument', 'local', 'static', 'constant',
                         'this', 'that', 'pointer', 'temp']
    
    def forward_pass(self):
        
        for line in self.file:
            if 'function' in line:
                words = line.split()
                self.current_func.append(words[1])

            if 'return' in line:
                self.current_func.pop(-1)

            if 'label' in line:
                words = line.split()
                new_label = self.current_func[-1] + '$' + words[1]
                line = line.replace(words[1], new_label)
                self.labels.append(new_label)
                            
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

    def second_pass(self):

        counter = 0
        for command in self.commands:
            if 'if-goto' in command:
                label = command[7:]
                for a_label in self.labels:
                    if label in a_label:
                        command = command.replace(label, a_label)
                        self.commands[counter] = command

            elif 'goto' in command:
                label = command[4:]
                for a_label in self.labels:
                    if label in a_label:
                        command = command.replace(label, a_label)
                        self.commands[counter] = command

            counter += 1
            
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

        if 'label' in self.pointer:
            return 'C_LABEL'

        if 'if-goto' in self.pointer:
            return 'C_IF'

        if 'goto' in self.pointer:
            return 'C_GOTO'

        if 'function' in self.pointer:
            return 'C_FUNCTION'

        if 'return' in self.pointer:
            return 'C_RETURN'

        if 'call' in self.pointer:
            return 'C_CALL'


    def arg1(self):

        for command in self.arithmetic_c:
            if command in self.pointer:
                return self.pointer

        for segment in self.segments:
            if segment in self.pointer:
                return segment

        if 'label' in self.pointer:
            return self.pointer[5:]

        if 'if-goto' in self.pointer:
            return self.pointer[7:]

        if 'goto' in self.pointer:
            return self.pointer[4:]
        
    def arg2(self):

        ret = ''
        for char in self.pointer:
            if char.isnumeric():
                ret += char

        return ret
        
