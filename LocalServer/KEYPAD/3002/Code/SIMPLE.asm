$mod186
$EP
NAME SIMPLETEST
;---------------------------------------------------------------------------

public	simpletest

$include(80188.inc)

SIMPLE	SEGMENT
ASSUME CS:SIMPLE

SIMPLETEST proc far
	
	PUSH AX
	PUSH BX
	PUSH CX
	PUSH DX
	
	
;OUTPUT:
	MOV DX, PORTA	;initialize BL for key code
	MOV AL, 00000000b
	OUT DX, AL	;clear all flags
	
	;jmp OUTPUT 
	;code called continuously in main file
	
	
	PUSH DX
	PUSH CX
	PUSH BX
	PUSH AX
	;ret
	
SIMPLETEST endp

SIMPLE	ENDS

END	

