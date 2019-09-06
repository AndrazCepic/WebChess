from poteza import Poteza
from bit import *

# Funkcije za generacijo začetne pozicije figur na šahovnici
def gen_zacetno_poz(tip):
    if tip == "w_k":
        # e1
        return koord_v_bit(4, 0)
    elif tip == "b_k":
        # e8
        return koord_v_bit(4, 7)    
    elif tip == "w_q":
        # d1
        return koord_v_bit(3, 0)
    elif tip == "b_q":
        # d8
        return koord_v_bit(3, 7)
    elif tip == "w_r":
        # a1 in h1
        return b_or(koord_v_bit(0, 0), koord_v_bit(7, 0))
    elif tip == "b_r":
        # a8 in h8
        return b_or(koord_v_bit(0, 7), koord_v_bit(7, 7))    
    elif tip == "w_b":
        # c1 in f1
        return b_or(koord_v_bit(2, 0), koord_v_bit(5, 0))
    elif tip == "b_b":
        # c8 in f8
        return b_or(koord_v_bit(2, 7), koord_v_bit(5, 7))
    elif tip == "w_n":
        # b1 in g1
        return b_or(koord_v_bit(1, 0), koord_v_bit(6, 0))
    elif tip == "b_n":
        # b8 in g8
        return b_or(koord_v_bit(1, 7), koord_v_bit(6, 7))        
    elif tip == "w_p":
        # a2 - h2
        bitb = 0    
        for x in range(8):
            bitb = b_or(bitb, koord_v_bit(x, 1))
        return bitb
    elif tip == "b_p":
        # a7 - h7
        bitb = 0
        for x in range(8):
            bitb = b_or(bitb, koord_v_bit(x, 6))
        return bitb
    return None

# Najde figure v bitboardu in vrne seznam pozicij teh figur
def najdi_figure(bitb):
    return [koord_v_bit(x, y) for y in range(8) for x in range(8) 
            if b_and(koord_v_bit(x, y), bitb)]

class Plosca:
    # Konstanti za beleženje, kdo je na potezi
    BELI = True
    CRNI = False

    # Indeksi za bitboarde posameznih tipov figur. 
    # Te se delijo na barvo(w = beli, b = črni) in tip figure(standardna notacija), 
    # torej na primer beli skakači ali pa črne dame.
    TIPI_FIGUR = {"w_k" : 0, "w_q" : 1, "w_r" : 2,
                  "w_b" : 3, "w_n" : 4, "w_p" : 5,
                  "b_k" : 6, "b_q" : 7, "b_r" : 8,
                  "b_b" : 9, "b_n" : 10, "b_p" : 11}

    def __init__(self):
        # Beleženje, kdo je na potezi
        self.barva = BELI

        # Hranjenje trenutnih pozicij figur v formatu bitboard.
        # Na šahovnici je 12 različnih tipov figur.
        # Za vsak tip posebej imamo pozicije figur tega tipa na šahovnici.
        # Te podatke hranimo v t.i bitboard implementaciji, 
        # kjer je šahovnica predstavljena kot 64 bitno število.
        self.figure = [0 for i in range(12)]
        
        # Generacija začetne šahovnice po vrsti kot je definirano zgoraj.
        for tip in TIPI_FIGUR:
            self.figure[TIPI_FIGUR[tip]] = gen_zacetno_poz(tip)

        # Seznam legalnih potez, tipa Poteza
        self.legalne_poteze = []

        # Beleženje zgodovine igre; seznam izvedenih potez skozi igro.
        # Pari objekta Poteza in INT za indeks zajete figure(None, če ni nobena).
        self.zgod_potez = []

        # Napadene pozicije na šahovnici 
        self.napadeni = 0

    # Vrne indeks tipa figure na poziciji ali None, če ni figure.
    # Argument je bitna pozicija
    def figura_na_poz(self, poz):
        if poz == None:
            return None

        for i in range(len(self.figure)):
            if b_and(self.figure[i], poz):
                return i
        return None

    # Vrne tip figure na poziciji
    # Argument je (x,y) pozicija
    def figura_na_poz_koord(self, x, y):
        return self.figura_na_poz(koord_v_bit(x, y))

    # Vrne True, če je poteza v seznamu legalnih
    def je_poteza_legalna(self, poteza):
        for pot in self.legalne_poteze:
            if poteza.enaka(pot):
                return True
        return False

    # Prebere potezo in osveži podatke šahovnice
    def zabelezi_potezo(self, poteza):
        if poteza.je_zajem():
            zajeti_poz = poteza.do
            if poteza.je_en_passant():
                # BELI: Zajeti kmet je 1 dol pod destinacijo kmeta (shift levo)
                # CRNI: Zajeti kmet je 1 gor nad destinacijo kmeta (shift desno)
                zajeti_poz = b_shift_l(poteza.do, 8) 
                                if self.barva == BELI 
                                else b_shift_d(poteza.do, 8)
            
            # Zabeležimo kateri tip figure je bil zajet
            for i in range(12):
                if self.figure[i] & zajeti_poz:
                    poteza.tip_zajete_fig = i
                    break

            # Zbrišemo zajeto figuro iz bitboarda
            self.figure = [b_and(bitb, b_not(zajeti_poz))
                            if b_and(bitb, zajeti_poz)
                            else bitb
                            for bitb in self.figure]

        if poteza.je_promocija():
            figura_prom = poteza.figura_prom() + int(self.barva == CRNI) * 6
            self.figure = [b_or(self.figure[i], poteza.do) 
                            if i == figura_prom
                            else b_and(self.figure[i], b_not(pozicija.od))
                            if b_and(self.figure[i], pozicija.od)
                            else self.figure[i]
                            for i in range(12)]
        elif poteza.je_rokada():
            # Kraljeva stran
            # Trdnjava je 1 desno od destinacije kralja
            # Premakne se pa 1 levo od destinacije kralja
            trdnjava_poz_od = b_shift_d(poteza.do, 1)
            trdnjava_poz_do = b_shift_l(poteza.do, 1)

            if poteza.flags == Poteza.ROKADA_Q:
                # Damina stran; popravek
                # Trdnjava je 2 levo od destinacije kralja
                # Premakne se pa 1 desno od destinacije kralja
                trdnjava_poz_od = b_shift_l(poteza.do, 2)
                trdnjava_poz_do = b_shift_d(poteza.do, 1)

            self.figure = [b_or(b_and(bitb, b_not(poteza.od)),poteza.do)
                        if b_and(bitb, poteza.od)
                        else b_or(b_and(bitb, b_not(trdnjava_poz_od)),trdnjava_poz_do)
                        if b_and(bitb, trdnjava_poz_od)
                        else bitb
                        for bitb in self.figure]
        else:
            self.figure = [b_or(b_and(bitb, b_not(poteza.od)),poteza.do)
                            if b_and(bitb, poteza.od)
                            else bitb
                            for bitb in self.figure]
        self.zgod_potez.append(poteza)

    # Razveljavi zadnjo zabeleženo potezo iz bitboarda
    def razveljavi_potezo(self):
        poteza = self.zgod_potez.pop()
        
        # Trenutna barva na vrsti(self.barva) je obratna od zadnje poteze
        barva = not self.barva

        # Zapišemo pobrisano figuro nazaj v bitboard
        if poteza.je_zajem():
            zajeti_poz = poteza.do
            if poteza.je_en_passant():
                # BELI: Zajeti kmet je 1 dol pod destinacijo kmeta (shift levo)
                # CRNI: Zajeti kmet je 1 gor nad destinacijo kmeta (shift desno)
                zajeti_poz = b_shift_l(poteza.do, 8) 
                                if barva == BELI 
                                else b_shift_d(poteza.do, 8)
            self.figure[poteza.tip_zajete_fig] = b_or(self.figure[poteza.tip_zajete_fig], 
                                                      zajeti_poz)
        
        if poteza.je_promocija():
            self.figure[poteza.figura_promocije()] = b_and(self.figure[poteza.figura_promocije()],
                                                           b_not(pozicija.do))
            # Posebej obravnavamo kmeta, 
            # saj iz destinacije ne moremo razbrati tipa pri promociji
            tip = TIPI_FIGUR["w_p"] if barva == BELI else TIPI_FIGUR["b_p"]
            self.figure[tip] = b_or(self.figure[tip], poteza.od)
        elif poteza.je_rokada():
            # Kraljeva stran
            # Trdnjava je 1 desno od destinacije kralja
            # Premakne se pa 1 levo od destinacije kralja
            trdnjava_poz_od = b_shift_d(poteza.do, 1)
            trdnjava_poz_do = b_shift_l(poteza.do, 1)

            if poteza.flags == Poteza.ROKADA_Q:
                # Damina stran; popravek
                # Trdnjava je 2 levo od destinacije kralja
                # Premakne se pa 1 desno od destinacije kralja
                trdnjava_poz_od = b_shift_l(poteza.do, 2)
                trdnjava_poz_do = b_shift_d(poteza.do, 1)

                self.figure = [b_or(b_and(bitb, b_not(poteza.do)), poteza.od)
                            if b_and(bitb, poteza.do)
                            else b_or(b_and(bitb, b_not(trdnjava_poz_do)), trdnjava_poz_od)
                            if b_and(bitb, trdnjava_poz_do)
                            else bitb
                            for bitb in self.figure]
        else:
            self.figure = [b_or(b_and(bitb, b_not(poteza.do)),poteza.od)
                                if b_and(bitb, poteza.do)
                                else bitb
                                for bitb in self.figure]

    # Nastavimo dodatne info glede na trenutno igro
    def prilagodi_potezo(self, poteza):
        tip = self.figura_na_poz(poteza.od)
        
        # Kmet
        if tip in (TIPI_FIGUR["w_p"], TIPI_FIGUR["b_p"]):
            # Dvojni premik kmeta; razlika v y je 2
            if poteza.do in (b_shift_d(poteza.od, 16), b_shift_l(poteza.od, 16)):
                poteza.flags = Poteza.DVOJNI_KMET
            # En Passant
            # Kmet eno nad ali pod tistim, ki se je prej premaknil za 2
            if self.zgod_potez[-1].je_dvojni_kmet():
                if poteza.do in (b_shift_l(self.zgod_potez[-1].do, 8), 
                                 b_shift_d(self.zgod_potez[-1].do, 8)):
                    poteza.flags = Poteza.EN_PASSANT
        # Kralj
        if tip in (TIPI_FIGUR["w_k"], TIPI_FIGUR["b_k"]):
            # Rokada; razlika v x je 2
            if poteza.do == b_shift_d(poteza.od, 2):
                poteza.flags = Poteza.ROKADA_K
            elif poteza.do == b_shift_l(poteza.od, 2):
                poteza.flags = Poteza.ROKADA_Q
        # Zajemi
        tip_fig_dest = self.figura_na_poz(poteza.do)
        if tip_fig_dest != None:
            poteza.flags = b_or(poteza.flags, Poteza.ZAJEM)
            poteza.tip_zajete_fig = tip_fig_dest

    # Generacija premikov za drseče figure(Q, R, B). Spustimo kralja
    def gen_drseci(self, zac_poz, dir_x, dir_y, barva):
        poz = koord_premik(zac_poz, dir_x, dir_y)
        tip_figure = self.figura_na_poz(poz)
        list_premiki = []
        # Dodamo prazne prostore
        while tip_figure in (None, TIPI_FIGUR["w_k"], TIPI_FIGUR["b_k"]) and poz != None:
            list_premiki.append(poz)
            poz = koord_premik(zac_poz, dir_x, dir_y)
            tip_figure = self.figura_na_poz(poz)
        # Dodamo zadnjega, ki je na šahovnici; ni prazen
        if pot != None:
            list_premiki.append(poz)
        return list_premiki

    # Generacija bitboarda napadenih potez
    def gen_napadene_poz(self):
        list_premikov = []
        fig_indeks = TIPI_FIGUR["b_k"] if self.barva == BELI else TIPI_FIGUR["w_k"]
        premik = 0

        # K; v vse smeri
        poz_list = najdi_figure(self.figure[fig_indeks])
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                premik = koord_premik(poz_list[0], x, y)
                if not (x == 0 and y == 0) and premik != None:
                    list_premikov.append(premik)
        # Q
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    # Vse smeri
                    if not (x == 0 and y == 0):
                        list_premikov += self.gen_drseci(poz, x, y, not self.barva)
        # R
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    # Samo hor. vert. smeri, torej en je 0
                    if not (x == 0 and y == 0) and (x == 0 or y == 0):
                        list_premikov += self.gen_drseci(poz, x, y, not self.barva)
        # B
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    # Samo diag, torej oba razlicna od 0
                    if x != 0 and y != 0:
                        list_premikov += self.gen_drseci(poz, x, y, not self.barva)
        # N
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-2, -1, 1, 2):
                for y in (-2, -1, 1, 2):
                    premik = koord_premik(poz, x, y)
                    # Nista oba premik za 1
                    if not (x in (-1, 1) and y in (-1, 1)) and premik != None:
                        list_premikov.append(premik)
        # P
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            # Napada lahko samo po diag
            for x in (-1, 1):
                premik = koord_premik(poz, x, 1)
                if premik != None:
                    list_premikov.append(premik)
        # Mergamo ta seznam napadenih pozicij v bitboard
        self.napadeni = 0
        for poz in list_premikov:
            self.napadeni = b_or(self.napadeni, poz)

    # Generacija legalnih potez
    def gen_legalne_poteze(self):
        self.legalne_poteze = []
        
        # K
        