from engine.plosca import Plosca, TIPI_FIGUR

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
        # Beleženje poteze
        self.plosca.zabelezi_potezo(poteza)
        if poteza.je_zajem():
            if self.plosca.barva:
                self.zajete_fig_beli.append(poteza.tip_zajete_fig)
            else:
                self.zajete_fig_crni.append(poteza.tip_zajete_fig)

        # Generacija novih legalnih potez za naslednjo potezo
        self.plosca.gen_legalne_poteze()

        # Nastavimo kdo je na potezi
        self.stanje_igre = int(not self.plosca.barva)

        # Ali je igre konec
        if len(self.plosca.legalne_poteze) == 0:
            if self.plosca.check:
                self.stanje_igre = STANJA["mat_beli" 
                                          if not self.plosca.barva
                                          else "mat_crni"]
            else:
                self.stanje_igre = STANJA["pat"]

    # Prejme UCI kodo poteze kot string
    # Vrne True, če je bila poteza legalna in izvedena
    # Vrne False, če je bila poteza ilegalna in se ni izvedla
    def izvedi_potezo_uci(self, uci):
        poteza = self.plosca.gen_pot_uci(uci)
        if not self.plosca.je_poteza_legalna(poteza):
            return False
        self.izvedi_potezo(poteza)
        return True

    def figura_na_poz(self, x, y):
        fig = self.plosca.figura_na_poz_koord(x, y)
        for key, val in TIPI_FIGUR.items():
            if val == fig:
                return key
        return None

    def v_uci(self, x1, y1, x2, y2):
        uci = chr(ord("a") + x1)
        uci += str(y1)
        uci += chr(ord("a") + x2)
        uci += str(y2)
        return uci


        
        