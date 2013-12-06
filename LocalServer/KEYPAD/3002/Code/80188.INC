;IO Setup for 80C188XL 
;By Zhu Shunyu

        UMCR    EQU    0FFA0H ; Upper Memory Control Register
        LMCR    EQU    0FFA2H ; Lower Memory control Register         
        PCSBA   EQU    0FFA4H ; Peripheral Chip Select Base Address
		MMCS	EQU	   0FFA6H ; Middle memory control register
        MPCS    EQU    0FFA8H ; MMCS and PCS Alter Control Register
		
	
	
		
; Initial 80C188XL UCS Pin
; |start address|block size| value for No waits, No Ready   
;   FE000H            8K                 3E04H
;   FC000H           16K                 3C04H
;   F8000H           32K                 3804H
 
         
; Initialize Upper Chip Select pin with 8K ROM 
        MOV DX, UMCR
        MOV AX, 03E04H
        OUT DX, AX

; Initialize Lower Chip Select pin with 8k RAM
        MOV DX, LMCR
        MOV AX, 01C4H  ; Starting address 1FFFH, 8K, No waits, last shoud be 5H for 1 waits      
		OUT DX, AL
		
; Initialize MPCS to MAP peripheral to IO address
         ;MOV DX, MPCS
         ;MOV AX, 2083H ; ;0010 0000 1000 0110; MMCS block size is 20H or 256KB, PCS programmed for I/O operation 
         ;OUT DX, AL
		 
; Initialize Middle Memory chip select
		;MOV 	DX, MMCS	; 
		;MOV 	AX, 3D03H	;0100 0000 0000 0110 ;no ready, 2 waits		
		;OUT 	DX, AX
		 
; PCSBA initial, set the serial port start from 00H
         MOV DX, PCSBA
         MOV AX, 0003H ; Peripheral starting address 00H no READY, No Waits
         OUT DX, AL



;Serial port definition and initialize 
         SRB     EQU       00H ; Serial Receiver Buffer Register (R)
         STB     EQU       00H ; Serial Transmitter Holding Register(W)  
         SIER    EQU       01H ; Serial Interrupte Enable Register (w)
         IIR     EQU       02H ; Interrupt Identification Register (R)
         SMD     EQU       03H ; Serial Line Control Register
         SST     EQU       05H ; Serial Line Status Register
         DLL     EQU       00H ; Divisor Latch Least Significant BYTE
         DLM     EQU       01H ; Divisor Latch most  Significant BYTE

;Definition of content of SST register
;|Not Use|TE|THRE|BI|FE|PE|OE|DR|
;TE Transmitter empty
;THRE Transmittor Holding Register Empty
;BI Breakr Interrupt
;FE Framing Error
;PE Parity Error
;OE Overrun Error 
;DR Data Ready
          REC_RDY    EQU   00000001B ;DR bit is 1
          TRAN_RDY   EQU   00100000B ;THRE bit is 1
          ERR_DET    EQU   00001110B ;set FE, PE and OE bits
          BREAK_DET  EQU   00010000B ;BI set
		  
;Line control register

; Serial Line Control Data
        SMD_DATA     EQU    00000111B ;
        S_INT_ENA    EQU    00000011B
        S_INT_DIS    EQU    00000000B
   
;1st bit set 1 to access the Divisor latch 
;2 stop bits, 8 data bits, no parity check
        SMD_DATA_DIV EQU    10000111B
; Set divisor value        
        MOV DX, SMD ;accessing the line control reg
        MOV AL, SMD_DATA_DIV ; bit 0 and 1 set to 11, means that each serial character rec or sent will be 8bits
							; bit 2 is set, which means that because characters are 8 bits, 2 stop bits are generated
							; bit 7 is the divisor access latch bit (DLAB)
        OUT DX, AL ; 
		
		; the divisor latch is basically a 16 bit register which holds the 16 bit number that helps set the baud rate 
		; divisor = input frequency/ ( desired baud rate * 16)
        MOV DX, DLL ;lower 8 bits of div latch
        MOV AL, 52
        OUT DX, AL
        MOV DX, DLM ;higher 8 bits of div latch. 
					;latch is set to 34h or 52d, which using a 16MHz crystal gives a baud rate of 19230
        MOV AL, 0
        OUT DX, AL
		
;SET SERIAL PORT WORKING MODE
         MOV DX, SMD ; line control register
         MOV AL, SMD_DATA ; same as previous, but bit 7 set to 0, ready for read or write operation
         OUT DX, AL
		 
;DISABLE SERIAL PORT INT
         MOV DX, SIER ;serial interrupt enable reg
         MOV AL, 0 ;all interrupts disables
         OUT DX, AL



; Timer control Unit
  
         T2_CON    EQU      0FF66H ; Timer 2 Control Register
         T2_CA     EQU      0FF62H ; Timer 2 compare register
         T2_CNT    EQU      0FF60H ;

         T1_CON    EQU      0FF5EH ; Timer 1 control
         T1_CB     EQU      0FF5CH ; Timer 1 compare B
         T1_CA     EQU      0FF5AH ; Timer 1 compare A
         T1_CNT    EQU      0FF58H ; Timer 1 counter
         
         T0_CON    EQU      0FF56H ;
         T0_CB     EQU      0FF54H ;
         T0_CA     EQU      0FF52H ;
         TO_CNT    EQU      0FF50H   
         
; Timer Control Data


;Interrupt Control Registers
      

	INT3_CTRL	EQU 0FF3EH ;Interrupt 3 Control Register
	INT2_CTRL	EQU 0FF3CH
	INT1_CTRL	EQU 0FF3AH
	INT0_CTRL	EQU 0FF38H
	TIMER_CTRL	EQU 0FF32H ;Timer Interrupt Control Register
	ISR			EQU 0FF30H ; Interrupt Status Register
	EOI         EQU 0FF22H ; END OF INTERRUPT REGISTER
	IMKW        EQU 0FF28H ; Interrupt Mask 
	IPMK        EQU 0FF2Ah ; Interrupt Priority Mask 

;| - | - | - | - |MSK|PM2|PM1|PM0| For TCU INT

;| - |SFNM|CAS|LVL|MSK|PM2|PM1|PM0| For TCU INT0,1

;MSK 1-enable, 0-mask int 
;pm0-pm1 Priority

