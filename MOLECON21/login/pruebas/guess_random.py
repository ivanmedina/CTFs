# v1 = randomf();
# v2 = (unsigned __int8)
#      (((unsigned __int64)v1 >> 56) + v1)
#      -
#      ((unsigned int)(v1 >> 31) >> 24);


def obt_cookie():
    eax = 1
    edx = eax >> 0x18
    cookie = (eax + edx) & MASK32
    cookie = cookie & MASK8
    cookie = (cookie + MASK32+1 - edx) & MASK8
    return cookie

print(obt_cookie())
