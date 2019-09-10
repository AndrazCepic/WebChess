from engine.poteza import *
from engine.bit import *

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

        # Ali je šah
        self.check = False

        # Potrebujemo za rokado
        # 0 - beli kraljeva
        # 1 - beli damina
        # 2 - črni kraljeva
        # 3 - črni damina
        self.pravice_rokade = [True, True, True, True]

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

    # Prebere potezo in osveži podatke šahovnice
    def zabelezi_potezo(self, poteza):
        # Figura, ki se premika
        fig = self.figura_na_poz(poteza.od)

        # Pravice rokade
        if fig == (TIPI_FIGUR["w_k"] if self.barva else TIPI_FIGUR["b_k"]):
            if self.pravice_rokade[0 if self.barva else 2]:
                poteza.spremeni_pravice_rokade[0 if self.barva else 2] = True
            if self.pravice_rokade[1 if self.barva else 3]:
                poteza.spremeni_pravice_rokade[1 if self.barva else 3] = True        
            self.pravice_rokade[0 if self.barva else 2] = False
            self.pravice_rokade[1 if self.barva else 3] = False
        if fig == (TIPI_FIGUR["w_r"] if self.barva else TIPI_FIGUR["b_r"]):
            # Kraljeva stran
            if poteza.od == koord_v_bit(7, 0 if self.barva else 7):
                if self.pravice_rokade[0 if self.barva else 2]:
                    poteza.spremeni_pravice_rokade[0 if self.barva else 2] = True
                self.pravice_rokade[0 if self.barva else 2] = False
            # Damina stran
            if poteza.od == koord_v_bit(0, 0 if self.barva else 7):
                if self.pravice_rokade[0 if self.barva else 2]:
                    poteza.spremeni_pravice_rokade[0 if self.barva else 2] = True
                self.pravice_rokade[0 if self.barva else 2] = False

        if poteza.je_zajem():
            zajeti_poz = poteza.do
            if poteza.je_en_passant():
                # BELI: Zajeti kmet je 1 dol pod destinacijo kmeta
                # CRNI: Zajeti kmet je 1 gor nad destinacijo kmeta
                zajeti_poz = (koord_premik(poteza.do, -1) 
                                if self.barva == BELI 
                                else koord_premik(poteza.do, -1))
            
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
            trdnjava_poz_od = koord_premik(poteza.do, 1, 0)
            trdnjava_poz_do = koord_premik(poteza.do, -1, 0)

            if poteza.flags == Poteza.ROKADA_Q:
                # Damina stran; popravek
                # Trdnjava je 2 levo od destinacije kralja
                # Premakne se pa 1 desno od destinacije kralja
                trdnjava_poz_od = koord_premik(poteza.do, -2, 0)
                trdnjava_poz_do = koord_premik(poteza.do, 1, 0)

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
        self.barva = not self.barva
        self.zgod_potez.append(poteza)

    # Razveljavi zadnjo zabeleženo potezo iz bitboarda
    def razveljavi_potezo(self):
        poteza = self.zgod_potez.pop()
        
        # Trenutna barva na vrsti(self.barva) je obratna od zadnje poteze
        barva = not self.barva

        # Pravice rokade
        for i in range(len(poteza.spremeni_pravice_rokade)):
            if poteza.spremeni_pravice_rokade[i]:
                self.pravice_rokade[i] = True

        # Zapišemo pobrisano figuro nazaj v bitboard
        if poteza.je_zajem():
            zajeti_poz = poteza.do
            if poteza.je_en_passant():
                # BELI: Zajeti kmet je 1 dol pod destinacijo kmeta
                # CRNI: Zajeti kmet je 1 gor nad destinacijo kmeta
                zajeti_poz = (koord_premik(poteza.do, -1) 
                              if barva == BELI 
                              else koord_premik(poteza.do, 1))
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
            trdnjava_poz_od = koord_premik(poteza.do, 1, 0)
            trdnjava_poz_do = koord_premik(poteza.do, -1, 0)

            if poteza.flags == Poteza.ROKADA_Q:
                # Damina stran; popravek
                # Trdnjava je 2 levo od destinacije kralja
                # Premakne se pa 1 desno od destinacije kralja
                trdnjava_poz_od = koord_premik(poteza.do, -2, 0)
                trdnjava_poz_do = koord_premik(poteza.do, 1, 0)

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
        self.barva = not self.barva

    # Nastavimo dodatne info glede na trenutno igro
    def prilagodi_potezo(self, poteza):
        tip = self.figura_na_poz(poteza.od)
        # Kmet
        if tip in (TIPI_FIGUR["w_p"], TIPI_FIGUR["b_p"]):
            # Dvojni premik kmeta; razlika v y je 2
            if poteza.do in (koord_premik(poteza.od, 0, 2), koord_premik(poteza.od, 0, -2)):
                poteza.flags = Poteza.DVOJNI_KMET
            # En Passant
            # Kmet eno nad ali pod tistim, ki se je prej premaknil za 2
            if self.zgod_potez[-1].je_dvojni_kmet():
                if poteza.do in (koord_premik(self.zgod_potez[-1].do, 0, -1), 
                                 koord_premik(self.zgod_potez[-1].do, 0, 1)):
                    poteza.flags = Poteza.EN_PASSANT
                    poteza.poz_zajete_fig = self.zgod_potez[-1].do
                    poteza.tip_zajete_fig = TIPI_FIGUR["b_p"] if self.barva else TIPI_FIGUR["b_p"] 
        # Kralj
        if tip in (TIPI_FIGUR["w_k"], TIPI_FIGUR["b_k"]):
            # Rokada; razlika v x je 2
            if poteza.do == koord_premik(poteza.od, 2, 0):
                poteza.flags = Poteza.ROKADA_K
            elif poteza.do == koord_premik(poteza.od, -2, 0):
                poteza.flags = Poteza.ROKADA_Q
        # Zajemi
        tip_fig_dest = self.figura_na_poz(poteza.do)
        if tip_fig_dest != None:
            poteza.flags = b_or(poteza.flags, Poteza.ZAJEM)
            poteza.tip_zajete_fig = tip_fig_dest
            poteza.poz_zajete_fig = poteza.do
        return poteza

    # Vrne True, če je poteza v seznamu legalnih
    def je_poteza_legalna(self, poteza):
        for pot in self.legalne_poteze:
            if poteza == pot:
                return True
        return False
    
    def gen_pot_uci(self, uci):
        return self.prilagodi_potezo(Poteza.gen_pot_uci(uci))

    # Generacija premikov za drseče figure(Q, R, B). Spustimo kralja
    # To so žarki v različne smeri podane z argumenti
    def gen_ray(self, zac_poz, dir_x, dir_y):
        poz = koord_premik(zac_poz, dir_x, dir_y)
        tip_figure = self.figura_na_poz(poz)
        list_premiki = []
        # Dodamo prazne prostore
        while tip_figure in (None, TIPI_FIGUR["w_k"], TIPI_FIGUR["b_k"]) and poz != None:
            list_premiki.append(poz)
            poz = koord_premik(zac_poz, dir_x, dir_y)
            tip_figure = self.figura_na_poz(poz)
        # Dodamo zadnjega, ki je na šahovnici; ni prazen
        if poz != None:
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
                        list_potez += [Poteza(poz, poz_do) 
                                       for poz_do in self.gen_ray(poz, x, y)]
        # R
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    # Samo hor. vert. smeri, torej en je 0
                    if not (x == 0 and y == 0) and (x == 0 or y == 0):
                        list_potez += [Poteza(poz, poz_do) 
                                       for poz_do in self.gen_ray(poz, x, y)]
        # B
        fig_indeks += 1
        poz_list = najdi_figure(self.figure[fig_indeks])
        for poz in poz_list:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    # Samo diag, torej oba razlicna od 0
                    if x != 0 and y != 0:
                        list_potez += [Poteza(poz, poz_do) 
                                       for poz_do in self.gen_ray(poz, x, y)]
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
            premik = koord_premik(poz, 0, 1 if barva else -1)
            if self.figura_na_poz(premik) == None and premik != None:
                # Še promocija
                if koord_y(premik) == (7 if barva else 0):
                    for i in range(4):
                        list_potez.append(Poteza(poz, premik, PROMOCIJA | i))
                else:
                    list_potez.append(Poteza(poz, premik))
            # 2 gor. tu zagotovo ni promocije
            premik = koord_premik(poz, 0, 2 if barva else -2)
            if self.figura_na_poz(premik) == None and premik != None:
                if koord_y(premik) == (1 if self.barva else 6):
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
                premik = koord_premik(poz, x, 1 if barva else -1)
                if premik != None:
                    list_potez.append(Poteza(poz, premik))
        return list_potez

    # Generacija legalnih potez
    def gen_legalne_poteze(self):
        self.legalne_poteze = []
        nap_poteze = self.gen_napadalne_poteze(not self.barva)
        # Zravnamo ta seznam napadenih pozicij v bitboard
        self.napadeni = 0
        for poteza in nap_poteze:
            self.napadeni = zapisi_v_bitb(self.napadeni, poteza.do)

        # Potencialne poteze za figure, ki niso kralj
        potencialne_poteze = self.gen_napadalne_poteze(self.barva)
        # Dodamo še gibanje kmetov, ki niso napadalne poteze
        potencialne_poteze += self.gen_kmet_potisk(self.bela)
        # Prilagodimo potencialne poteze
        potencialne_poteze = [self.prilagodi_potezo(poteza) for poteza in potencialne_poteze]

        # K
        poz_list = najdi_figure(self.figure[TIPI_FIGUR["w_k"]] 
                                if self.barva
                                else self.figure[TIPI_FIGUR["b_k"]])
        poz_kralj = poz_list[0]

        # Odstranimo pinane figure
        # TODO
        # Filtriramo napade drsečih figur
        ray_cast_nasp = 0
        for pot in nap_poteze:
            # Je drseča, ki napada
            if self.figura_na_poz(pot.od) in range(TIPI_FIGUR["b_q"] if self.barva 
                                                   else TIPI_FIGUR["w_q"], 
                                                   TIPI_FIGUR["b_b"] if self.barva 
                                                   else TIPI_FIGUR["w_b"]):
                # Ali je med kraljem in to figuro
                if pot.do in ray_cast(pot.od, poz_kralj):
                    ray_cast_nasp = zapisi_v_bitb(ray_cast_nasp, pot.do)
        # Žarek kralja v vse smeri
        ray_cast_kralj = [poz for dx in (1, 0, -1)
                              for dy in (1, 0, -1)
                              for poz in gen_ray(poz_kralj, dx, dy)
                              if not (dx == 0 and dy == 0)]
        # Bitboard žarkov kralja
        ray_cast_kralj_bitb = 0
        for poz in ray_cast_kralj:
                ray_cast_kralj_bitb = zapisi_v_bitb(ray_cast_kralj_bitb, poz)
        # Pinane figure so na pozicijah, kjer se žarka napadalnih figur in od kralja sekata
        pin_bitb = b_and(ray_kralj_bitb, ray_cast_nasp)

        # Lahko se zgodi, da je presek dveh žarkov kar žarek, kadar je šah,
        # kar pa se lahko zgodi le natanko tedaj, ko so ta polja None,
        # zato še odstranimo polja iz pin_bitb, ki so None
        pin_poz = najdi_figure(pin_bitb)
        for poz in pin_poz:
            if self.figura_na_poz(poz) == None:
                pin_bitb = odstrani_iz_bitb(pin_bitb, poz)
        pin_poz = najdi_figure(pin_bitb)

        # Odstranimo pinano figuro iz bitboarda in ray castamo od kralja v smeri te figure,
        # da dobimo možne legalne poteze pinane figure
        neveljavne_pot = []
        # Odstranitev pin_bitb iz vseh bitboardov za ray cast od kralja
        temp_fig = [bitb for bitb in self.figure]
        self.figure = [odstrani_iz_bitb(bitb, pin_bitb)
                       for bitb in self.figure]
        for poz in pin_poz:
            # Ray cast od kralja
            x1, y1 = koord_poz(poz_kralj)
            x2, y2 = koord_poz(poz)
            dif_x = x2 - x1
            dif_y = y2 - y1
            dir_x = 1 if dif_x > 0 else 0 if dif_x == 0 else -1
            dir_y = 1 if dif_y > 0 else 0 if dif_y == 0 else -1
            ray = self.gen_ray(poz_kralj, dir_x, dir_y)

            # Neveljavne poteze iz potencialnih potez
            for pot in potencialne_poteze:                
                if pot.od == poz and pot.do not in ray:
                    neveljavne_pot.append(pot)

        # Odstranimo še En Passant poteze,
        # ki jih algoritem za pin ne zazna
        for pot in potencialne_poteze:
            if pot.je_en_passant():
                # Tak en passant je odkrit napad na kralja
                if (je_v_bitb(ray_cast_nasp, pot.poz_zajete_fig) and
                    je_v_bitb(ray_cast_kralj_bitb, pot.od)):
                    neveljavne_pot.append(pot)
                if (je_v_bitb(ray_cast_nasp, pot.od) and
                    je_v_bitb(ray_cast_kralj_bitb, pot.poz_zajete_fig)):
                    neveljavne_pot.append(pot)    

        # Vrnitev figur v prvotno stanje
        self.figure = temp_fig

        # Odstranimo neveljavne poteze iz potencialnih
        potencialne_poteze = [pot for pot in potencialne_poteze 
                              if pot not in neveljavne_pot]

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

        # Rokada - kraljeva stran
        if self.rokada_dovoljena[0 if self.barva else 2]:
            poz_1 = koord_premik(poz_kralj, 1, 0)
            poz_2 = koord_premik(poz_kralj, 2, 0)
            if (self.figura_na_poz(poz_1) == None and
                self.figura_na_poz(poz_2) == None):
                # Preverimo, če sta poziciji napadeni
                if (not je_v_bitb(self.napadeni, poz_1) and
                    not je_v_bitb(self.napadeni, poz_2)):
                    self.legalne_poteze.append(self.prilagodi_potezo(Poteza(poz_kralj, poz_2)))
        # Rokada - damina stran
        if self.rokada_dovoljena[1 if self.barva else 3]:
            poz_1 = koord_premik(poz_kralj, -1, 0)
            poz_2 = koord_premik(poz_kralj, -2, 0)
            if (self.figura_na_poz(poz_1) == None and
                self.figura_na_poz(poz_2) == None):
                # Preverimo, če sta poziciji napadeni
                if (not je_v_bitb(self.napadeni, poz_1) and
                    not je_v_bitb(self.napadeni, poz_2)):
                    self.legalne_poteze.append(self.prilagodi_potezo(Poteza(poz_kralj, poz_2)))

        # Ostale poteze; Zajemi veljajo le, če je zajeta figura tuja
        for poteza in potencialne_poteze:
            if poteza.od == poz_kralj:
                # Kralja smo že obravnavali
                continue
            if poteza.je_zajem():
                if poteza.tip_zajete_fig in range(0 if self.barva else 6, 
                                                  6 if self.barva else 12):
                    # Spustimo poteze, ki so zajemi svoje barve
                    continue
            if (self.figura_na_poz(poteza.od) == 
               (TIPI_FIGUR["w_p"] if self.barva else TIPI_FIGUR["b_p"])):
                if not poteza.je_en_passant():
                    if self.figura_na_poz(poteza.do) == None:
                        if poteza.do not in (koord_premik(poteza.od, 0, 1 if self.barva else -1), 
                                             koord_premik(poteza.od, 0, 2 if self.barva else -2)):
                            # Kmet se je premaknil po diagonali, vendar ni zajem,
                            # zato ga izpustimo
                            continue
            self.legalne_poteze.append(poteza)