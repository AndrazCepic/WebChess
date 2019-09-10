from engine.bit import *

# Maske tipov potez
QUIET = int("0b0000", 2)
DVOJNI_KMET = int("0b0001", 2)
ROKADA_K = int("0b0010", 2)
ROKADA_Q = int("0b0011", 2)
EN_PASSANT = int("0b0101", 2)
ZAJEM = int("0b0100", 2)
PROMOCIJA = int("0b1000", 2)
FIGURE_P = int("0b0011", 2)

# String oznake za figure pri promociji
PROM_STR = {"q" : 0, "r" : 1, "b" : 2, "n" : 3}

class Poteza:
    def __init__(self, od, do, flags = QUIET):
        self.od = od
        self.do = do
        self.flags = flags
        self.tip_zajete_fig = None
        self.poz_zajete_fig = None
        self.spremeni_pravice_rokade = [False, False, False, False]

    def je_promocija(self):
        return (self.flags & PROMOCIJA) != 0

    def je_rokada(self):
        return self.flags == ROKADA_K or self.flags == ROKADA_Q

    def je_en_passant(self):
        return self.flags == EN_PASSANT

    # Ang. capture
    def je_zajem(self):
        return (self.flags & ZAJEM) != 0

    def je_dvojni_kmet(self):
        return self.flags == DVOJNI_KMET

    # Vrne indeks tipa figure v skladu z definicijo v Plosca
    # Prva dva bita določata figuro.
    # Q = 0, R = 1, B = 2, N = 3
    def figura_promocije(self):
        return (self.flags & FIGURE_P) + 1

    # Enakost potez objektno
    def eq(self, pot2):
        return (self.od == pot2.od and
                self.do == pot2.do)

    # Poteze iz UCI šahovski notaciji(string) v objekt Poteza
    @staticmethod
    def gen_pot_uci(uci):
        # Preverimo dolžino
        if len(uci) not in [4, 5]:
            return None

        x1 = ord(uci[0]) - ord("a")
        x2 = ord(uci[2]) - ord("a")
        y1 = int(uci[1])
        y2 = int(uci[3])

        # Preverimo koordinate
        if not all(x in range(8) for x in [x1, x2, y1, y2]):
            return None

        poz_od = koord_v_bit(x1, y1)
        poz_do = koord_v_bit(x2, y2)

        # Promocija
        if len(uci) == 5:
            # Preverimo string
            if uci[4] not in PROM_STR:
                return None
            return Poteza(poz_od, poz_do, b_or(PROMOCIJA, PROM_STR[uci[4]]))
        return Poteza(poz_od, poz_do)

        