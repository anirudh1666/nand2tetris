# The code class for virtual machine in Hack.

class Code:

    def __init__(self):

        self.writer = None
        self.filename = None


    def set_file_name(self, name):

        self.writer = open(name, 'w')
        self.filename = name
        self.unique_label = 0        # Handles multiple arithmetic operations so if you have double
                                     # equality each one has a unique label.

    # Used to get value at memory address pointed by stack pointer and
    # store it in D register and then decrement SP.
    def decrement_sp(self):

        self.writer.write('@SP\n')            # SP = Stack pointer
        self.writer.write('AM=M-1\n')
        self.writer.write('D=M\n')            # Store value in data register.

    # Stores the value in D register into the RAM[sp + 1] and then increments
    # sp.
    def increment_sp(self):

        self.writer.write('@SP\n')            # Go to stack pointer.
        self.writer.write('A=M\n')            # Go to address.
        self.writer.write('M=D\n')            # Store value in D reg into memory.
        self.writer.write('@SP\n')
        self.writer.write('M=M+1\n')

    # Writes arithmetic assembly code. R13 holds rhs and data register holds
    # lhs.
    def write_arithmetic(self, command):

        self.decrement_sp()

        # Check if unary if so compute operation and push to stack.
        if command == 'neg':
            self.writer.write('D=-D\n')
            self.increment_sp()
            return

        if command == 'not':
            self.writer.write('D=!D\n')
            self.increment_sp()
            return 

        # Store Data register value in RAM[13]. Stores lhs of expression.
        self.writer.write('@R13\n')
        self.writer.write('M=D\n')

        self.decrement_sp()

        self.writer.write('@R13\n')
        if command == 'add':
            self.writer.write('D=M+D\n')
            self.increment_sp()
        elif command == 'sub':
            self.writer.write('D=D-M\n')
            self.increment_sp()
        elif command == 'eq':
            self.writer.write('D=D-M\n')
            self.writer.write('@eqtrue' + str(self.unique_label) + '\n')
            self.writer.write('D;JEQ\n')

            # Not equal to zero so push false to stack.
            self.writer.write('D=0\n')
            self.increment_sp()
            self.writer.write('@eqend' + str(self.unique_label) + '\n')
            self.writer.write('0;JMP\n')

            # if lhs - rhs = 0 then jump here and push true to stack.
            self.writer.write('(' + 'eqtrue' + str(self.unique_label) + ')\n')
            self.writer.write('D=-1\n')
            self.increment_sp()

            self.writer.write('(' + 'eqend' + str(self.unique_label) + ')\n')
            self.unique_label += 1
            
        elif command == 'gt':
            self.writer.write('D=D-M\n')
            self.writer.write('@gttrue' + str(self.unique_label) + '\n')
            self.writer.write('D;JGT\n')

            # if lhs - rhs is not > 0, push false to stack.
            self.writer.write('D=0\n')
            self.increment_sp()
            self.writer.write('@gtend' + str(self.unique_label) + '\n')
            self.writer.write('0;JMP\n')

            # if lhs > rhs push -1 to stack.
            self.writer.write('(' + 'gttrue' + str(self.unique_label) + ')\n')
            self.writer.write('D=-1\n')
            self.increment_sp()

            self.writer.write('(gtend' + str(self.unique_label) + ')\n')
            self.unique_label += 1
            
        elif command == 'lt':
            self.writer.write('D=D-M\n')
            self.writer.write('@lttrue' + str(self.unique_label) + '\n')
            self.writer.write('D;JLT\n')

            # if lhs - rhs is not < 0, push false to stack.
            self.writer.write('D=0\n')
            self.increment_sp()
            self.writer.write('@ltend' + str(self.unique_label) + '\n')
            self.writer.write('0;JMP\n')

            # if lhs < rhs push -1 to stack.
            self.writer.write('(' + 'lttrue' + str(self.unique_label) + ')\n')
            self.writer.write('D=-1\n')
            self.increment_sp()

            self.writer.write('(ltend' + str(self.unique_label) + ')\n')
            self.unique_label += 1
            
        elif command == 'and':
            self.writer.write('D=D&M\n')
            self.increment_sp()
        elif command == 'or':
            self.writer.write('D=D|M\n')
            self.increment_sp()


    def write_push_pop(self, command, segment, index):

        if command == 'push':
            if segment == 'argument':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.writer.write('@ARG\n')
                self.writer.write('A=M+D\n')
                self.writer.write('D=M\n')
                self.increment_sp()

            elif segment == 'local':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.writer.write('@LCL\n')
                self.writer.write('A=M+D\n')
                self.writer.write('D=M\n')
                self.increment_sp()

            elif segment == 'constant':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.increment_sp()

            elif segment == 'this':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.writer.write('@THIS\n')
                self.writer.write('A=M+D\n')
                self.writer.write('D=M\n')
                self.increment_sp()

            elif segment == 'that':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.writer.write('@THAT\n')
                self.writer.write('A=M+D\n')
                self.writer.write('D=M\n')
                self.increment_sp()

            elif segment == 'pointer':
                self.writer.write('@' + str(index + 3) + '\n')
                self.writer.write('D=M\n')
                self.increment_sp()

            elif segment == 'temp':
                self.writer.write('@' + str(index + 5) + '\n')
                self.writer.write('D=M\n')
                self.increment_sp()

            elif segment == 'static':
                self.writer.write('@' + self.filename + '.' + str(index) + '\n')
                self.writer.write('D=M\n')
                self.increment_sp()

        elif command == 'pop':
            if segment == 'argument':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.writer.write('@ARG\n')
                self.writer.write('D=M+D\n')
                self.writer.write('@R13\n')
                self.writer.write('M=D\n')
                self.decrement_sp()
                self.writer.write('@R13\n')
                self.writer.write('A=M\n')
                self.writer.write('M=D\n')

            elif segment == 'local':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.writer.write('@LCL\n')
                self.writer.write('D=M+D\n')
                self.writer.write('@R13\n')
                self.writer.write('M=D\n')
                self.decrement_sp()
                self.writer.write('@R13\n')
                self.writer.write('A=M\n')
                self.writer.write('M=D\n')

            elif segment == 'this':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.writer.write('@THIS\n')
                self.writer.write('D=M+D\n')
                self.writer.write('@R13\n')
                self.writer.write('M=D\n')
                self.decrement_sp()
                self.writer.write('@R13\n')
                self.writer.write('A=M\n')
                self.writer.write('M=D\n')

            elif segment == 'that':
                self.writer.write('@' + str(index) + '\n')
                self.writer.write('D=A\n')
                self.writer.write('@THAT\n')
                self.writer.write('D=M+D\n')
                self.writer.write('@R13\n')
                self.writer.write('M=D\n')
                self.decrement_sp()
                self.writer.write('@R13\n')
                self.writer.write('A=M\n')
                self.writer.write('M=D\n')

            elif segment == 'pointer':
                self.decrement_sp()
                self.writer.write('@' + str(index + 3) + '\n')
                self.writer.write('M=D\n')

            elif segment == 'temp':
                self.decrement_sp()
                self.writer.write('@' + str(index + 5) + '\n')
                self.writer.write('M=D\n')

            elif segment == 'static':
                self.decrement_sp()
                self.writer.write('@' + self.filename + '.' + str(index) + '\n')
                self.writer.write('M=D\n')

    def close(self):

        self.writer.close()
