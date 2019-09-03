class Plosca:
    # Indeksi za bitboarde posameznih tipov figur. 
    # Te se delijo na barvo in tip figure, 
    # torej na primer beli skakac ali pa črne dame.
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
    BC_KMET = 11

    # MSB 1 ostali 0 za 64 bit INT je v HEX:
    # 0x8000000000000000
    MSB = int("0x8000000000000000", 0)

    def __init__(self):
        # Hranjenje trenutnih pozicij figur v formatu bitboard.
        # Na šahovnici je 12 različnih tipov figur.
        # Za vsak tip posebej imamo pozicije figur tega tipa na šahovnici.
        # Te podatke hranimo v t.i bitboard implementaciji, 
        # kjer je šahovnica predstavljena kot 64 bitno število
        self.figure = []
        
        # Seznam legalnih potez, tipa Poteza
        self.legalne_poteze = []

        # Napadene pozicije na šahovnici 
        self.napadeni = c_longlong(0)

    def iz_koord_v_bit(x, y):
        # MSB je pozicija a1. 
        # X narašča v desno. SHIFT desno za x
        # Y narašča gor. SHIFT desno za y*8, 
        # saj y vrstic gor, vsaka ta pa je 8 bitov
        return (MSB >> x) >> y*8

    def osvezi_plosco(poteza):
        
    