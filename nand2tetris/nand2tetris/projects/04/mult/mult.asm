// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)


// This algorithm works by adding R0 to R2 (starting value = 0) R1 times.

	@2
	M=0              // Load zero into R2 
	@LOOP
	0;JMP
(LOOP)
	@1               // Check if R2 == 0. If so then go to end.
	D=M  
	@END
	D;JEQ  
	@0               // Otherwise, R2 = R2 + R1 
	D=M
	@2 
	M=D+M
	@1               // Decrement R2. 
	M=M-1
	@LOOP 
	0;JMP
(END)
	@END
	0;JMP
	

