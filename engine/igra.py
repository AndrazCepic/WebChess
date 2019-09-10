from engine.plosca import Plosca

class Igra:
    # Konstante za beleženje stanja igre.
    # V_TEKU - Igra teče in ni končana
    # MAT_BELI - Beli je zmagal igro in matiral črnega
    # MAT_CRNI - Črni je zmagal igro in matiral belega
    # PAT - Igra je končana in je izenačeno
    STANJA = {"v_teku" : 0,
              "mat_beli" : 1,
              "mat_crni" : 2,
              "pat" : 3}

    def __init__(self):
        self.stanje_igre = self.STANJA["v_teku"]
        self.plosca = Plosca()
        self.zajete_fig_beli = []
        self.zajete_fig_crni = []

    def nova_igra(self):
        self.stanje_igre = self.STANJA["v_teku"]
        self.plosca = Plosca()
        self.zajete_fig_beli = []
        self.zajete_fig_crni = []

    def izvedi_potezo(self, poteza):
        self.plosca.zabelezi_potezo(poteza)
        if poteza.je_zajem():
            if self.plosca.barva:
                self.zajete_fig_beli.append(poteza.tip_zajete_fig)
            else:
                self.zajete_fig_crni.append(poteza.tip_zajete_fig)
        self.plosca.gen_legalne_poteze()
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



        
        