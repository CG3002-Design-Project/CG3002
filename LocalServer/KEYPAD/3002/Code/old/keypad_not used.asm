$mod186
$EP
NAME KEYPAD
;---------------------------------------------------------------------------

extrn	print_char:far
public	keypad

$include(80188.inc)

;DATA_SEG	SEGMENT
	;button      DB  '1', '2', '3','1', '2', '3'
;DATA_SEG	ENDS

KEYPAD_ROUTINE	SEGMENT
ASSUME CS:KEYPAD_ROUTINE

keypad proc far

	PUSH    DX
	PUSH	CX
	PUSH 	BX
	PUSH	AX


SETUP:		

	MOV CL, 07FH ;01111111 Row output to ground from PB
	MOV CH, 0H	;set row counter



NEXTROW:		
		ROL CL, 01H  ;rotate CL to ground next row/ al HAS 8 BITS. so must JMP BACK TO WAIT

		MOV AL,CL
		MOV DX, PORTB	;port B address to DX; 
		OUT DX, AL	;ground one of the rows
                
		MOV DX, PORTC	;port B address to DX  
		IN  AL,DX		;read input port for key closure


		XOR AL, 00111111b	;PC0 to PC5 masked. Whichever one is 0 will give a 1 output
		
		CMP AL,0H 	;checking for no key is pressed
	   	JE RETPOINT
		
		;ERROR CHECK
		CMP AL, 00000001B ;PC0 pressed
		JE VALIDATED
		CMP AL, 00000010B ;PC1 pressed
		JE VALIDATED
		CMP AL, 00000100B ;PC2 pressed
		JE VALIDATED
		CMP AL, 00001000B ;PC3 pressed
		JE VALIDATED
		CMP AL, 00010000B ;PC4 pressed
		JE VALIDATED
		CMP AL, 00100000B ;PC5 pressed
		JE VALIDATED
		
		JMP RETPOINT ;invalid keypress of some kind

VALIDATED:		
		
		
		;AND AL, 07H; MASK OTHER BLOODY BITS OMGOMGOMG
		
		SHR AL,01 ; shifting right gives you the col number, the first col on the keypad being col 0
		MOV DL,AL ; this col number goes into DL

		;Logic: (Row number * 6) + col number 
		;gives us the so called button number being pressed, which can be stored as
		;an array starting at the top left of the keypad and ending at the bottom right
		
		mov AL,CH ; row number, previously saved
		MOV DH,06
		;multiply AL by DH, result stored in AX
		MUL DH

		
		ADD AL, DL ;Add row*6 to col to get button number
		MOV BL,AL
		XOR BH,BH
		;BL now has the button number

NUMBERS:

		MOV AL, 02H; Stores character in AL (?)
		XOR AH,AH
		CALL FAR PTR PRINT_CHAR

              		
RETPOINT:	
	INC CH
	CMP CH,04
	JNZ NEXTROW
	JMP SETUP


	POP AX
	POP BX
	POP CX
	POP DX
	ret

keypad endp


KEYPAD_ROUTINE	ENDS

END
