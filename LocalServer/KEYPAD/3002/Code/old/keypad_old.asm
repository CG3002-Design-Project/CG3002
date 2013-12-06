	NAME EG0_COMP

;IO Setup for 80C188 
	UMCR    EQU    0FFA0H ; Upper Memory Control Register
	LMCR    EQU    0FFA2H ; Lower Memory control Register         
	PCSBA   EQU    0FFA4H ; Peripheral Chip Select Base Address
	MPCS    EQU    0FFA8H ; MMCS and PCS Alter Control Register
	IOPORT  EQU    00080H
	
	; STACK SEGMENT
	STACK_SEG		SEGMENT
		
	STACK_SEG		ENDS
		
		
	; DATA SEGMENT
	DATA_SEG        SEGMENT 
	DATA_SEG        ENDS

	; RESET SEGMENT
	Reset_Seg   SEGMENT
		MOV DX, UMCR
		MOV AX, 03E07H
		OUT DX, AX
		JMP far PTR start
		
	Reset_Seg  ends
	; MESSAGE SEGMENT
	MESSAGE_SEG     SEGMENT
	MESSAGE_SEG     ENDS
	;CODE SEGMENT
	CODE_SEG        SEGMENT
		   
	PUBLIC	START
	ASSUME  CS:CODE_SEG, DS:DATA_SEG, SS:STACK_SEG
	START:	
	
	; Initialize MPCS to MAP peripheral to IO address
	MOV DX, MPCS
	MOV AX, 0083H
	OUT DX, AX
; PCSBA initial, set the parallel port start from 00H
	MOV DX, PCSBA
	MOV AX, 0003H ; Peripheral starting address 00H no READY, No Waits
	OUT DX, AX
; Initialize LMCS 
    MOV DX, LMCR
    MOV AX, 01C4H  ; Starting address 1FFFH, 8K, No waits, last shoud be 5H for 1 waits      
    OUT DX, AX
	; YOUR CODE HERE ...
	; GOOD LUCK!
	
	mov ax, data_seg
	mov ds,ax
	mov es,ax
	PORTB EQU 00081h ; Port B
	PORTC EQU 00082h;  Port C
	CWR  EQU 00083h ; address
	

	STARTK:		MOV AL, 89H       ;mode 0, B - out, C-in, A - out --- C- output port
				MOV DX, 8003H
				OUT DX, AL	;send the control word
			
				MOV BL, 00H	;initialize BL for key code
				XOR AX, AX	;clear all flags
				MOV DX, 8001H  ;port B address to DX
				OUT DX, AL	;ground all rows
			
				MOV DX, 8002H	;Port C address to DX

	WAITK:		IN AL, DX	;read all columns
				AND AL, 3FH	;Mask data lines D7-D6 -- we use all the 6 columns together
				
				CMP AL, 0FH  ;any key pressed?
				JZ WAITK		;if not, wait till key press
				CALL DEBOUNCE ;wait for 10ms if key press
				MOV AL, 07FH	;load data byte to ground a row
				MOV BH, 04H	;set row counter
				
	NXTROW:	ROL AL, 01H       ;rotate AL to ground next row
			MOV CH, AL	;save data byte to ground next row
			MOV DX, 8001H	;port B address to DX
			OUT DX, AL	;ground one of the rows
			
			MOV DX, 8002H	;port C address to DX
			IN AL, DX	;read input port for key closure
			AND AL, 3FH	;Mask D4-D7
			MOV CL, 04H	;set column counter
			
	NXTCOL:	RCR AL, 01H       ;move D0 to CF
			JNC CODEKY	;key closure is found, if CF=0
			INC BL		;inc BL for next binary key code
			DEC CL		;dec column counter if no key closure
			
			JNZ NXTCOL	;check for key closure in next column
			MOV AL, CH	;Load data byte to ground next row
			DEC BH		;if no key closure found in all columns in this row, go to ground next row
			
			JNZ NXTROW	;go back to ground next row
			JMP WAITK	;back to check for key closure again

	CODEKY:	MOV AL, BL	;key code is transferred to AL
			MOV AH, 4CH	;return to DOS prompt
			INT 21H		;

;This procedure generates 10ms delay at 5MHz
;operating frequency, which corresponds to 
;50,000 clock cycles.

	DEBOUNCE PROC NEAR
		PUSH CX
				
	Option1:	MOV CX, 094Ch ; 2380 dec
	BACK:		NOP	  ; 3 clocks
				LOOP BACK; 18 clocks
		POP CX
		RET
	DEBOUNCE ENDP
	
CODE_SEG ENDS
END
			
