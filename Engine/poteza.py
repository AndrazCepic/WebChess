class Poteza:
    def __init__(self, od_poz, do_poz, napred):
        # Začetna pozicija in končna pozicija kot para celih števil
        self.od_poz = od_poz
        self.do_poz = do_poz

        # Možno napredovanje kmeta
        self.napred = napred

    # Parsanje(prevajanje) poteze v UCI šahovski notaciji(torej tipa string) v objekt Poteza
    def iz_uci_v_poteza(poteza_uci):
        


