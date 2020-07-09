// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


	@count          // SCREEN[count] tells us which part to black out or clear.
	M=0
	@LOOP 
	0;JMP 

(LOOP)
	@KBD            // Listen for keyboard input. If KBD != 0 blackout.
	D=M 
	@BLACKOUT
	D;JNE 
	
	@count          // Checks if there are any pixels that we need to black out. 
	D=M             // Does this by checking if counter < 0. 
	@LOOP 
	D;JLT
	
	@count          // This part clears the screen. Goes to SCREEN[count]
	D=M             // and sets that value to 0. Then it decrements count.
	@SCREEN
	A=D+A
	M=0
	@count 
	M=M-1 
	@LOOP 
	0;JMP 
	
(BLACKOUT)
	@count          // This part blacks out. First it checks if count is out of bounds
	D=M             // there are 8192 consecutive registers for screen. So if count >
	@store          // 8192 then go to loop. Else you go to SCREEN[count] and set it 
	M=D             // to -1 which turns it black. Then decrement count.
	@8192
	D=A 
	@store 
	D=M-D
	@LOOP 
	D;JEQ
	
	@count 
	D=M 
	@SCREEN
	A=D+A 
	M=-1
	@count 
	M=M+1
	@LOOP
	0;JMP
	
	
	
	