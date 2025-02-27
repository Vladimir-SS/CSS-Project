; Example program

; Assignment
MOV R1, #67       ; Move immediate value 10 to register R1
MOV R2, R1        ; Move value from R1 to R2
MOV R3, #2       ; Move value from R1 to R2
MOV M10, R2
MOV M11, MR2

; Addition, Subtraction, Multiplication, Division
ADD R1, R2    ; Add value of R2 to R1, store result in R1
SUB R2, R1    ; Subtract value of R1 from R2, store result in R2
MUL R3, R5    ; Multiply value of R5 with R3, store result in R3
DIV R4, R1    ; Divide value of R4 by R1, store result in R4

; Boolean Operations
NOT R1        ; Bitwise NOT operation on R1, store result in R1
AND R1, R2    ; Bitwise AND operation between R1 and R2, store result in R1
OR R2, R3     ; Bitwise OR operation between R2 and R3, store result in R2
XOR R4, R5    ; Bitwise XOR operation between R4 and R5, store result in R4
SHL R6, #2    ; Shift value of R6 left by 2 positions, store result in R6

MOV M12 M4095 ; reading from the keyboard

; Comparison
CMP R3, R4        ; Compare values of R3 and R4, set flags based on the relation

; Conditional Jumps based on the flags set by the previous comparison
JE label1        ; Jump to label1 if equal flag is set
JG label2        ; Jump to label2 if greater than flag is set
JL label3        ; Jump to label3 if less than flag is set
JGE label4        ; Jump to label4 if greater than or equal flag is set
JLE label5        ; Jump to label5 if less than or equal flag is set
JNE label6        ; Jump to label6 if not equal flag is set

label1:           ; Define label1
  ; Code block for label1

label2:           ; Define label2
  ; Code block for label2

label3:           ; Define label3
  ; Code block for label3

label4:           ; Define label4
  ; Code block for label4

label5:           ; Define label5
  ; Code block for label5

label6:           ; Define label6
  ; Code block for label6

; Push/Pop
PUSH R1           ; Push value of R1 onto the stack
POP R2            ; Pop value from the stack and store in R2

; Function Call/Return
CALL function1    ; Call function1

; Unconditional Jump
JMP end_program   ; Unconditional jump to the end of the program

function1:        ; Define function1
MOV R6, #20
MOV R5, #10
MOV R4, #0
RET              ; Return from function1

end_program:      ; End of program