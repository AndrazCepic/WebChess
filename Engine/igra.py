from plosca import Plosca

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
        # Stanje igre
        self.stanje_igre = STANJA["v_teku"]

        # Instaca pozicij figur
        self.plosca = Plosca()

    # Vrne True, če je bila poteza legalna in izvedena
    # Vrne False, če je bila poteza ilegalna in se ni izvedla
    def izvedi_potezo(poteza):
        if not plosca.poteza_legalna():
            