# This is the SymbolTable module for nand2tetris assembler.

class SymbolTable:

    def __init__(self):

        self.table = {
            'SP' : format(0, 'b').zfill(15),
            'LCL' : format(1, 'b').zfill(15),
            'ARG' : format(2, 'b').zfill(15),
            'THIS' : format(3, 'b').zfill(15),
            'THAT' : format(4, 'b').zfill(15),
            'R0' : format(0, 'b').zfill(15),
            'R1' : format(1, 'b').zfill(15),
            'R2' : format(2, 'b').zfill(15),
            'R3' : format(3, 'b').zfill(15),
            'R4' : format(4, 'b').zfill(15),
            'R5' : format(5, 'b').zfill(15),
            'R6' : format(6, 'b').zfill(15),
            'R7' : format(7, 'b').zfill(15),
            'R8' : format(8, 'b').zfill(15),
            'R9' : format(9, 'b').zfill(15),
            'R10' : format(10, 'b').zfill(15),
            'R11' : format(11, 'b').zfill(15),
            'R12' : format(12, 'b').zfill(15),
            'R13' : format(13, 'b').zfill(15),
            'R14' : format(14, 'b').zfill(15),
            'R15' : format(15, 'b').zfill(15),
            'SCREEN' : format(16384, 'b').zfill(15),
            'KBD' : format(24576, 'b').zfill(15)
            }

    def add_entry(self, symbol, address):

        self.table[symbol] = address

    def contains(self, symbol):

        if symbol in self.table:
            return True

        return False

    def get_address(self, symbol):

        return self.table[symbol]
