from bit import *

class Poteza:
    # Konstanta, da poteza ni napredovanje kmeta.
    # -1, saj je 0-11 zasedeno za indekse figur
    NE_NAPRED = -1

    def __init__(self, od, do, napred = NE_NAPRED):
        # Začetna pozicija in končna pozicija
        self.od = od
        self.do = do

        # Možno napredovanje kmeta.
        # Je indeks tipa figure v katerega napreduje
        self.napred = napred

    def napreduje(self):
        return self.napred != NE_NAPRED

    # Poteze iz UCI šahovski notaciji(torej tipa string) v objekt Poteza
    def uci_v_poteza(self, poteza_uci):
        


