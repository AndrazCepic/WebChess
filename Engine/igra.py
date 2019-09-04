from plosca import Plosca

class Igra:
    # Konstante za beleženje stanja igre.
    # V_TEKU - Igra teče in ni končana
    # MAT_BELI - Beli je zmagal igro in matiral črnega
    # MAT_CRNI - Črni je zmagal igro in matiral belega
    # PAT - Igra je končana in je izenačeno
    V_TEKU = 0
    MAT_BELI = 1
    MAT_CRNI = 2
    PAT = 3


    def __init__(self):
        # Beleženje, kdo je na potezi
        self.poteza = BELI

        # Stanje igre
        self.stanje_igre = V_TEKU

        # Instaca pozicij figur
        self.plosca = Plosca()

        # Beleženje zgodovine igre; seznam izvedenih potez skozi igro
        self.zgod_potez = []

    # Vrne True, če je bila poteza legalna in izvedena
    # Vrne False, če je bila poteza ilegalna in se ni izvedla
    def izvedi_potezo(poteza):
