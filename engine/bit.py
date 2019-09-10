from ctypes import c_ulonglong
from functools import lru_cache


# Python dela z signed int, mi pa potrebujemo unsigned
def sign_v_unsign(x):
    return c_ulonglong(x).value


# MSB 1 ostali 0 za 64 bit INT je v HEX:
# 0x8000000000000000
MSB = sign_v_unsign(int("0x8000000000000000", 0))


# Wrapper osnovnih binarnih operacij,
# da ni povsod klicanja sign_v_unsign drugje
def b_and(x, y):
    return sign_v_unsign(x & y)


def b_or(x, y):
    return sign_v_unsign(x | y)


def b_not(x):
    return sign_v_unsign(~x)


# Shift desno za x mest: stev >> x
def b_shift_d(stev, x):
    return sign_v_unsign(stev >> x)


# Shift levo za x mest: stev << x
def b_shift_l(stev, x):
    return sign_v_unsign(stev << x)


def je_v_bitb(bitb, poz):
    return b_and(bitb, poz) != 0


def odstrani_iz_bitb(bitb, poz):
    return b_and(bitb, b_not(poz))


def zapisi_v_bitb(bitb, poz):
    return b_or(bitb, poz)


def koord_v_bit(x, y):
    # MSB je pozicija a1.
    # X narašča v desno. SHIFT desno za x
    # Y narašča gor. SHIFT desno za y*8,
    # saj y vrstic gor, vsaka ta pa je 8 bitov
    return sign_v_unsign((MSB >> x) >> y * 8)


# Maski za koordinati
x_maska = 0
y_maska = 0
for i in range(8):
    x_maska = b_or(x_maska, koord_v_bit(0, i))
    y_maska = b_or(y_maska, koord_v_bit(i, 0))


@lru_cache(maxsize=None)
def koord_y(poz):
    y = 0
    y_maska_it = y_maska
    while not je_v_bitb(y_maska_it, poz):
        y_maska_it = b_shift_d(y_maska_it, 8)
        y += 1
    return y


@lru_cache(maxsize=None)
def koord_x(poz):
    x = 0
    x_maska_it = x_maska
    while not je_v_bitb(x_maska_it, poz):
        x_maska_it = b_shift_d(x_maska_it, 1)
        x += 1
    return x


@lru_cache(maxsize=None)
def koord_premik(poz, x, y):
    if ((koord_x(poz) + x not in range(8))
            or (koord_y(poz) + y) not in range(8)):
        return None
    if x >= 0:
        if y >= 0:
            return b_shift_d(b_shift_d(poz, x), y * 8)
        else:
            return b_shift_l(b_shift_d(poz, x), abs(y) * 8)
    else:
        if y >= 0:
            return b_shift_d(b_shift_l(poz, abs(x)), y * 8)
        else:
            return b_shift_l(b_shift_l(poz, abs(x)), abs(y) * 8)


def koord_poz(poz):
    return (koord_x(poz), koord_y(poz))


# Žarek med figurama. Vrne pozicije med pozicijama
# Deluje diagonalno, horizontalno ali pa vertikalno
@lru_cache(maxsize=None)
def ray_cast(od, do):
    x1, y1 = koord_poz(od)
    x2, y2 = koord_poz(do)
    dif_x = x2 - x1
    dif_y = y2 - y1
    if not (abs(dif_x) == abs(dif_y) or dif_x == 0 or dif_y == 0):
        # Ni diagonala, horizontala ali pa vertikala
        return 0

    dir_x = 1 if dif_x > 0 else 0 if dif_x == 0 else -1
    dir_y = 1 if dif_y > 0 else 0 if dif_y == 0 else -1
    ray_poz = 0
    poz = koord_premik(od, dir_x, dir_y)
    while poz != do:
        ray_poz = zapisi_v_bitb(ray_poz, poz)
        poz = koord_premik(poz, dir_x, dir_y)
    return ray_poz
