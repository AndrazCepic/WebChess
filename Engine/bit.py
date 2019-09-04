from ctypes import c_ulonglong

# MSB 1 ostali 0 za 64 bit INT je v HEX:
# 0x8000000000000000
MSB = c_ulonglong(int("0x8000000000000000", 0))

# Python dela z signed int, mi pa potrebujemo unsigned
def sign_v_unsign(x):
    return c_ulonglong(x).value

def koord_v_bit(x, y):
    # MSB je pozicija a1. 
    # X narašča v desno. SHIFT desno za x
    # Y narašča gor. SHIFT desno za y*8, 
    # saj y vrstic gor, vsaka ta pa je 8 bitov
    return sign_v_unsign((MSB >> x) >> y*8)

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
