MOV R1, #65       ; Move immediate value 10 to register R1
MOV R2, R1        ; Move value from R1 to R2
MOV R3, #97       ; Move value from R1 to R2
MOV M10, R2
MOV M11, R3
MOV M50, R1

CMP R2, R3
CALL label
MOV R7, #10
MOV R7, #10
MOV R7, #10

label:
MOV R6, #20
MOV R5, #10
MOV R4, #0
RET

end: