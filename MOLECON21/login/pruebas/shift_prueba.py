def shr(dest, count=1):
    return dest >> count

noshr=0xaaa
sishr=shr(0xaaa)

print(hex(noshr),'->',bin(noshr))
print(hex(sishr),'->',bin(sishr))

# mov eax, 0xA  ; set EAX to 0xA (1010 in binary)
# shr eax, 2    ; shifts 2 bits to the right in EAX, now equal to 0x2 (0010 in binary)
#               +---+---+---+---+---┬───┬───┬───┬───┐
# mov eax, 0xA  | 0 | 0 | 0 | 0 | 0 │ 1 │ 0 │ 1 │ 0 │
#               +---+---+---+---+---┴───┴───┴───┴───┘
#                                     │   │   └───────────┐
#                                     │   └───────┐       │
#                                     └───────┐   │       │
#               +---+---+---+---+---+---+---┬───┬───┐   ┌───┐
# shr eax, 2    | 0 | 0 | 0 | 0 | 0 | 0 | 0 │ 1 │ 0 │   │ 1 │
#               +---+---+---+---+---+---+---┴───┴───┘   └───┘
#                                                         CF
# shr eax, 1   ;Signed division by 2
# shr eax, 2   ;Signed division by 4
# shr eax, 3   ;Signed division by 8
# shr eax, 4   ;Signed division by 16
# shr eax, 5   ;Signed division by 32
# shr eax, 6   ;Signed division by 64
# shr eax, 7   ;Signed division by 128
# shr eax, 8   ;Signed division by 256