from poteza import Poteza
from bit import *

# Funkcije za generacijo začetne pozicije figur na šahovnici
def gen_kralj(barva):
    if barva:
        # e1
        return koord_v_bit(4, 0)
    # e8
    return koord_v_bit(4, 7)

def gen_dama(barva):
    if barva:
        # d1
        return koord_v_bit(3, 0)
    # d8
    return koord_v_bit(3, 7)

def gen_trdnjava(barva):
    if barva:
        # a1 in h1
        return b_or(koord_v_bit(0, 0), koord_v_bit(7, 0))
    # a8 in h8
    return b_or(koord_v_bit(0, 7), koord_v_bit(7, 7))

def gen_lovec(barva):
    if barva:
        # c1 in f1
        return b_or(koord_v_bit(2, 0), koord_v_bit(5, 0))
    # c8 in f8
    return b_or(koord_v_bit(2, 7), koord_v_bit(5, 7))  

def gen_skakac(barva):
    if barva:
        # b1 in g1
        return b_or(koord_v_bit(1, 0), koord_v_bit(6, 0))
    # b8 in g8
    return b_or(koord_v_bit(1, 7), koord_v_bit(6, 7))      

def gen_kmet(barva):
    bitb = 0
    if barva:
        # a2 - h2
        for x in range(8):
            bitb = b_or(bitb, koord_v_bit(x, 1))
        return bitb
    # a7 - h7
    for x in range(8):
        bitb = b_or(bitb, koord_v_bit(x, 6))
    return bitb

class Plosca:
    # Konstanti za beleženje, kdo je na potezi
    BELI = True
    CRNI = False

    # Indeksi za bitboarde posameznih tipov figur. 
    # Te se delijo na barvo in tip figure, 
    # torej na primer beli skakači ali pa črne dame.
    B_KRALJ = 0
    B_DAMA = 1
    B_TRDNJAVA = 2
    B_LOVEC = 3
    B_SKAKAC = 4
    B_KMET = 5

    C_KRALJ = 6
    C_DAMA = 7
    C_TRDNJAVA = 8
    C_LOVEC = 9
    C_SKAKAC = 10
    C_KMET = 11

    def __init__(self):
        # Hranjenje trenutnih pozicij figur v formatu bitboard.
        # Na šahovnici je 12 različnih tipov figur.
        # Za vsak tip posebej imamo pozicije figur tega tipa na šahovnici.
        # Te podatke hranimo v t.i bitboard implementaciji, 
        # kjer je šahovnica predstavljena kot 64 bitno število
        self.figure = []
        
        # Generacija začetne šahovnice po vrsti kot je definirano zgoraj
        figure.append(gen_kralj(BELI))
        figure.append(gen_dama(BELI))
        figure.append(gen_trdnjava(BELI))
        figure.append(gen_lovec(BELI))
        figure.append(gen_skakac(BELI))
        figure.append(gen_kmet(BELI))

        figure.append(gen_kralj(CRNI))
        figure.append(gen_dama(CRNI))
        figure.append(gen_trdnjava(CRNI))
        figure.append(gen_lovec(CRNI))
        figure.append(gen_skakac(CRNI))
        figure.append(gen_kmet(CRNI))

        # Seznam legalnih potez, tipa Poteza
        self.legalne_poteze = []

        # Napadene pozicije na šahovnici 
        self.napadeni = 0

    # Prebere potezo in osveži podatke šahovnice
    def zabelezi_potezo(self, poteza):
        if not poteza.napreduje():
            self.figure = [b_or(b_and(bitb, b_not(poteza.od)),poteza.do)
                            if b_and(bitb, poteza.od)
                            else bitb
                            for bitb in self.figure]
        else:
            self.figure = [b_or(self.figure[i], poteza.do) 
                            if i == poteza.napred
                            else b_and(self.figure[i], b_not(pozicija.od))
                            if b_and(self.figure[i], pozicija.od)
                            else self.figure[i]
                            for i in range(12)]
    
    def razveljavi_potezo(self, poteza):
        
    