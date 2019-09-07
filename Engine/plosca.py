from poteza import *
from bit import *

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
            if je_v_bitb(bitb, koord_v_bit(x, y))]

def je_fig_drseca(self, fig):
    return fig in (TIPI_FIGUR["w_q"], TIPI_FIGUR["w_r"], TIPI_FIGUR["w_b"],
                       TIPI_FIGUR["b_q"], TIPI_FIGUR["b_r"], TIPI_FIGUR["b_b"])

class Plosca:
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
        self.check = False

    # Vrne indeks tipa figure na poziciji ali None, če ni figure.
    # Argument je bitna pozicija
    def figura_na_poz(self, poz):
        if poz == None:
            return None

        for i in range(len(self.figure)):
            if je_v_bitb(self.figure[i], poz):
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
                            if je_v_bitb(bitb, zajeti_poz)
                            else bitb
                            for bitb in self.figure]

        if poteza.je_promocija():
            figura_prom = poteza.figura_prom() + int(self.barva == CRNI) * 6
            self.figure = [b_or(self.figure[i], poteza.do) 
                            if i == figura_prom
                            else b_and(self.figure[i], b_not(pozicija.od))
                            if je_v_bitb(self.figure[i], pozicija.od)
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
                        if je_v_bitb(bitb, poteza.od)
                        else b_or(b_and(bitb, b_not(trdnjava_poz_od)),trdnjava_poz_do)
                        if je_v_bitb(bitb, trdnjava_poz_od)
                        else bitb
                        for bitb in self.figure]
        else:
            self.figure = [b_or(b_and(bitb, b_not(poteza.od)),poteza.do)
                            if je_v_bitb(bitb, poteza.od)
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
                            if je_v_bitb(bitb, poteza.do)
                            else b_or(b_and(bitb, b_not(trdnjava_poz_do)), trdnjava_poz_od)
                            if je_v_bitb(bitb, trdnjava_poz_do)
                            else bitb
                            for bitb in self.figure]
        else:
            self.figure = [b_or(b_and(bitb, b_not(poteza.do)),poteza.od)
                                if je_v_bitb(bitb, poteza.do)
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
                if poteza.do in (koord_premik(self.zgod_potez[-1].do, 0, -1), 
                                 koord_premik(self.zgod_potez[-1].do, 0, 1)):
                    poteza.flags = Poteza.EN_PASSANT
                    poteza.poz_zajete_fig = self.zgod_potez[-1].do
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
            poteza.poz_zajete_fig = poteza.do
        return poteza

    # Generacija premikov za drseče figure(Q, R, B). Spustimo kralja
    # To so žarki v različne smeri podane z argumenti
    def gen_ray(self, zac_poz, dir_x, dir_y, barva):
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

    # Generacija potez drsečih figur za barvo
    def gen_drseci(self, barva):
        list_potez = []
        fig_indeks = TIPI_FIGUR["w_q" if barva else "b_q"]
        # Q
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    # Vse smeri
                    if not (x == 0 and y == 0):
                        list_potez += [Poteza(poz, poz_do) for poz_do in self.gen_ray(poz, x, y, barva)]
        # R
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    # Samo hor. vert. smeri, torej en je 0
                    if not (x == 0 and y == 0) and (x == 0 or y == 0):
                        list_potez += [Poteza(poz, poz_do) for poz_do in self.gen_ray(poz, x, y, barva)]
        # B
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    # Samo diag, torej oba razlicna od 0
                    if x != 0 and y != 0:
                        list_potez += [Poteza(poz, poz_do) for poz_do in self.gen_ray(poz, x, y, barva)]
        return list_potez

    # Poteze skakačev
    def gen_skakac(self, barva):
        list_potez = []
        poz_list = najdi_figure(self.figure[TIPI_FIGUR["w_n" if barva else "b_n"]])
        for poz in poz_list:
            for x in (-2, -1, 1, 2):
                for y in (-2, -1, 1, 2):
                    premik = koord_premik(poz, x, y)
                    # Nista oba premik za 1
                    if not (x in (-1, 1) and y in (-1, 1)) and premik != None:
                        list_potez.append(Poteza(poz, premik))
        return list_potez

    def gen_kmet_potisk(self, barva):
        list_potez = []
        poz_list = najdi_figure(self.figure[TIPI_FIGUR["w_p" if barva else "b_p"]])
        for poz in poz_list:
            # 1 gor
            premik = koord_premik(poz, 0, 1)
            if self.figura_na_poz(premik) == None and premik != None:
                # Še promocija
                if koord_y == (7 if barva else 1):
                    for i in range(4):
                        list_potez.append(Poteza(poz, premik, PROMOCIJA | i))
                else:
                    list_potez.append(Poteza(poz, premik))
            # 2 gor. tu zagotovo ni promocije
            premik = koord_premik(poz, 0, 2)
            if self.figura_na_poz(premik) == None and premik != None:
                if koord_y(premik) == (2 if self.barva else 7):
                    list_potez.append(Poteza(poz, premik))
        return list_potez

    # Generacija bitboarda napadenih potez
    def gen_napadalne_poteze(self, barva):
        list_potez = []
        fig_indeks = TIPI_FIGUR["w_k"] if barva else TIPI_FIGUR["b_k"]
        premik = 0

        # K; v vse smeri
        poz_list = najdi_figure(self.figure[fig_indeks])
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                premik = koord_premik(poz_list[0], x, y)
                if not (x == 0 and y == 0) and premik != None:
                    list_potez.append(Poteza(poz_list[0], premik))
        # Drseči. Barva bo nasprotnikova
        list_potez += self.gen_drseci(barva)
        # N
        list_potez += self.gen_skakac(barva)
        # P
        poz_list = najdi_figure(self.figure[TIPI_FIGUR["w_p" if barva else "b_p"]])
        for poz in poz_list:
            # Napada lahko samo po diagonali
            for x in (-1, 1):
                premik = koord_premik(poz, x, 1)
                if premik != None:
                    list_potez.append(Poteza(poz, premik))
        return list_potez

    # Generacija legalnih potez
    def gen_legalne_poteze(self):
        self.legalne_poteze = []
        nap_poteze = self.gen_napadalne_poteze(not self.barva)
        # Mergamo ta seznam napadenih pozicij v bitboard
        self.napadeni = 0
        for poteza in nap_poteze:
            self.napadeni = b_or(self.napadeni, poteza.do)

        # Pinane figure

        # K
        poz_list = najdi_figure(self.figure[TIPI_FIGUR["w_k"] 
                                if self.barva == BELI
                                else self.figure[TIPI_FIGUR["b_k"]])
        poz_kralj = poz_list[0]
        # Poteze kralja
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                premik = koord_premik(poz_kralj, x, y)
                if not (x == 0 and y == 0) and premik != None:
                    # Legalnost
                    if (not je_v_bitb(self.napadeni, premik) and
                            self.figura_na_poz(premik) not in 
                            range(1 if self.barva else 7, 6 if self.barva else 12)):
                        self.legalne_poteze.append(self.prilagodi_potezo(Poteza(poz_kralj, premik)))
        # Ali je šah. Shranimo napadalce polja kralja
        check_poteze = []
        for poteza in nap_poteze:
            if poteza.do == poz_kralj:
                check_poteze.append(poteza)

        self.check = True
        if len(check_poteze) > 1:
            # Dvojni šah. Legalne so samo poteze kralja, 
            # saj nobena figura ne more zajeti več kot ene na enkrat
            # Smo že obravnavali te poteze, torej samo končamo postopek
            return
        elif len(check_poteze) == 1:
            # Katera figura daje šah
            poz_napad = check_poteze[0].od
            # Ali je drseča
            poz_vmes = 0
            if je_fig_drseca(self.figura_na_poz(poz_napad)):
                poz_vmes = ray_cast(poz_napad, poz_kralj)
            
            potencialne_poteze = self.gen_napadalne_poteze(self.barva)
            # Dodamo še gibanje kmetov, ki niso napadalne poteze
            potencialne_poteze += self.gen_kmet_potisk(self.bela)
            potencialne_poteze = [self.prilagodi_potezo(poteza) for poteza in potencialne_poteze]

            # Dodamo poteze, ki zajamejo napadalno figuro,
            # ali pa blokirajo napad, če je napadalna drseča
            for poteza in potencialne_poteze:
                # TODO: PINANE FIGURE NISO VELJAVNE!!!
                if poteza.je_zajem():
                    if poteza.poz_zajete_fig == poz_napad:
                        self.legalne_poteze.append(poteza)
                if je_v_bitb(poz_vmes, poteza.do):
                    self.legalne_poteze.append(poteza)
            return
        self.check = False

        # Ostale poteze
        
        