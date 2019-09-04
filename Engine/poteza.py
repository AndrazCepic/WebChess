from bit import *

class Poteza:
    # Flags tipov potez
    QUIET = int("0b0000", 2)
    DVOJNI_KMET = int("0b0001", 2)
    ROKADA_K = int("0b0010", 2)
    ROKADA_Q = int("0b0011", 2)
    ZAJEM = int("0b0100", 2)
    EN_PASSANT = int("0b0101", 2)
    PROM_Q = int("0b1000", 2)
    PROM_R = int("0b1001", 2)
    PROM_B = int("0b1010", 2)
    PROM_N = int("0b1011", 2)
    PROM_ZAJEM_Q = int("0b1100", 2)
    PROM_ZAJEM_R = int("0b1101", 2)
    PROM_ZAJEM_B = int("0b1110", 2)
    PROM_ZAJEM_N = int("0b1111", 2)

    # Maske tipov potez
    PROMOCIJA = int("0b1000", 2)
    ZAJEM = int("0b0100", 2)
    FIGURE_P = int("0b0011", 2)

    def __init__(self, od, do, flags = QUIET):
        self.od = od
        self.do = do
        self.flags = flags

    def je_promocija(self):
        return self.flags & PROMOCIJA != 0

    def je_rokada(self):
        return self.flags == ROKADA_K or self.flags == ROKADA_Q

    def je_en_passant(self):
        return self.flags == EN_PASSANT

    # Ang. capture
    def je_zajem(self):
        return (self.flags & ZAJEM) != 0

    # Vrne indeks tipa figure v skladu z def. v Plosca
    def figura_promocije(self):
        return (self.flags & FIGURE_P) + 1

    # Poteze iz UCI šahovski notaciji(torej tipa string) v objekt Poteza
    def gen_iz_uci(self, poteza_uci):
        


