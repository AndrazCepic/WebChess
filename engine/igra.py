from engine.plosca import *
from engine.bit import *

class Igra:
    # Konstante za beleženje stanja igre.
    # V_TEKU - Igra teče in ni končana
    # MAT_BELI - Beli je zmagal igro in matiral črnega
    # MAT_CRNI - Črni je zmagal igro in matiral belega
    # PAT - Igra je končana in je izenačeno
    STANJA = {"beli_pot" : 0,
              "crni_pot" : 1,
              "mat_beli" : 2,
              "mat_crni" : 3,
              "pat" : 4}

    def __init__(self):
        self.stanje_igre = self.STANJA["beli_pot"]
        self.plosca = Plosca()
        self.zajete_fig_beli = []
        self.zajete_fig_crni = []
        self.plosca.gen_legalne_poteze()


    def new_game(self):
        self.stanje_igre = self.STANJA["beli_pot"]
        self.plosca = Plosca()
        self.zajete_fig_beli = []
        self.zajete_fig_crni = []
        self.plosca.gen_legalne_poteze()


    def izvedi_potezo(self, poteza):
        if poteza.je_zajem():
            if self.plosca.barva:
                self.zajete_fig_beli.append(poteza.tip_zajete_fig)
            else:
                self.zajete_fig_crni.append(poteza.tip_zajete_fig)
        # Beleženje poteze
        self.plosca.zabelezi_potezo(poteza)
        # Generacija novih legalnih potez za naslednjo potezo
        self.plosca.gen_legalne_poteze()
        # Nastavimo kdo je na potezi
        self.stanje_igre = self.STANJA["beli_pot" 
                                  if self.plosca.barva
                                  else "crni_pot"]
        # Ali je igre konec
        if len(self.plosca.legalne_poteze) == 0:
            if self.plosca.check:
                self.stanje_igre = self.STANJA["mat_beli" 
                                          if not self.plosca.barva
                                          else "mat_crni"]
            else:
                self.stanje_igre = self.STANJA["pat"]


    def fig_v_str(self, fig):
        for key, val in TIPI_FIGUR.items():
            if val == fig:
                return key
        return None


    def figura_na_poz(self, x, y):
        fig = self.plosca.figura_na_poz_koord(x, y)
        for key, val in TIPI_FIGUR.items():
            if val == fig:
                return key
        return None


    def v_uci(self, x1, y1, x2, y2):
        uci = chr(ord("a") + x1)
        uci += str(y1 + 1)
        uci += chr(ord("a") + x2)
        uci += str(y2 + 1)
        return uci


    def izpisi_legalne_poteze(self):
        for pot in self.plosca.legalne_poteze:
            print("Figura: " + self.figura_na_poz(koord_x(pot.od), koord_y(pot.od)) + 
                  " od (" + str(koord_x(pot.od)) + ", " + str(koord_y(pot.od)) + ") " + 
                  "do (" + str(koord_x(pot.do)) + ", " + str(koord_y(pot.do)) + ")")        
    

    def izpisi_napadene_poz(self):
        for poz in najdi_figure(self.plosca.napadeni):
            print(str(koord_poz(poz)))