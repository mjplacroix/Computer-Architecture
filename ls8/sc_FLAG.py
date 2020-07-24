"""
This is an instruction handled by the ALU.

CMP registerA registerB

Compare the values in two registers.

If they are equal, set the Equal E flag to 1, otherwise set it to 0.

If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.



00000LGE
"""
flag = 0b000000100
flag2 = flag
flag2 -= 1
print(flag2)
flag2 = flag2 >> 2
print(flag2)
