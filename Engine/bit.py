from ctypes import c_ulonglong

# Python dela z signed int, mi pa potrebujemo unsigned
def sign_v_unsign(x):
    return c_ulonglong(x).value

# MSB 1 ostali 0 za 64 bit INT je v HEX:
# 0x8000000000000000
MSB = sign_v_unsign(int("0x8000000000000000", 0))

def koord_v_bit(x, y):
    # MSB je pozicija a1. 
    # X narašča v desno. SHIFT desno za x
    # Y narašča gor. SHIFT desno za y*8, 
    # saj y vrstic gor, vsaka ta pa je 8 bitov
    return sign_v_unsign((MSB >> x) >> y*8)

def koord_premik(poz, x, y):
    if (koord_x(poz) + x not in range(8)) or
       (koord_y(poz) + y) not in range(8)):
       return None

    if x >= 0:
        if y >= 0:
            return sign_v_unsign((poz >> x) >> y*8)
        else:
            return sign_v_unsign((poz >> x) << (-y)*8)
    else
        if y >= 0:
            return sign_v_unsign((poz << (-x)) >> y*8)
        else:
            return sign_v_unsign((poz << (-x)) << (-y)*8)

def koord_y(poz):
    count = 0
    while poz != 0:
        poz = sign_v_unsign(poz << 8)
        count += 1
    return count
    
def koord_x(poz):
    count = 0
    y = koord_y(poz)
    while koord_y(poz) == y:
        poz = sign_v_unsign(poz << 1)
        count += 1
    return count

def koord_poz(poz):
    return (koord_x(poz), koord_y(poz))

# Wrapper osnovnih binarnih operacij,
# da ni povsod klicanja sign_v_unsign drugje
def b_and(x, y):
    return sign_v_unsign(x & y)

def b_or(x, y)
    return sign_v_unsign(x | y)

def b_not(x):
    return sign_v_unsign(~x)

# Shift desno za x mest: stev >> x
def b_shift_d(stev, x):
    return sign_v_unsign(stev >> x)

# Shift levo za x mest: stev << x
def b_shift_l(stev, x):
    return sign_v_unsign(stev << x)
