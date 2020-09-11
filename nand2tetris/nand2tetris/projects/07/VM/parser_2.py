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
        self.forward_pass()
        self.second_pass()
        self.arithmetic_c = ['add', 'sub', 'neg', 'eq', 'gt',
                             'lt', 'and', 'or', 'not']
        self.segments = ['argument', 'local', 'static', 'constant',
                         'this', 'that', 'pointer', 'temp']
        
    def forward_pass(self):
        
        for line in self.file:
            line = line.replace('\n','')
            line = line.replace('\t','')
            if '//' in line:
                index = line.index('//')
                line = line[:index]
                
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

            line = line.replace('\t', '')
            line = line.replace('\n', '')
            if '//' in line:
                index = line.index('//')
                line = line[:index]
            if line.replace(' ','') == '':
                continue
            self.commands.append(line)
            continue

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

        if 'function' in self.pointer:
            return 'C_FUNCTION'

        if 'call' in self.pointer:
            return 'C_CALL'

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

        if 'return' in self.pointer:
            return 'C_RETURN'

        for command in self.arithmetic_c:
            if command in self.pointer:
                return 'C_ARITHMETIC'


    # @returns = first argument in VM line.
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
            a_label = self.pointer[8:].replace(' ', '')
            for label in self.labels:
                if a_label in label:
                    return label

        elif 'goto' in self.pointer:
            a_label = self.pointer[5:].replace(' ', '')
            for label in self.labels:
                if a_label in label:
                    return label

    # @returns = second argument in VM line if applicable.
    def arg2(self):

        ret = ''
        for char in self.pointer:
            if char.isnumeric():
                ret += char

        return ret

    # @returns = function name
    # This is only called when Vm line calls function or is executing one.
    def arg1func(self):

        words = self.pointer.split()
        return words[1]


    # @returns = nVars or nArgs in function depending on VM line.
    # Only called when VM line calls function or is executing one.
    def arg2func(self):

        words = self.pointer.split()
        return int(words[2])
        
