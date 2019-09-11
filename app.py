import bottle
from engine.igra import Igra

igra = Igra()
is_start_sq = True
from_sq = "00"
to_sq = "00"
promotion_w = False
promotion_b = False
prom_uci = None

# Debug
debug_str = ""


@bottle.route("/")
def index():
    return bottle.template("index", igra=igra, 
                           prom_w=promotion_w, 
                           prom_b=promotion_b)


@bottle.post("/board_input")
def board_input():
    global from_sq, to_sq, is_start_sq, promotion_w, promotion_b, prom_uci
    sq = bottle.request.forms.get("click")
    if is_start_sq:
        from_sq = sq
    else:
        to_sq = sq
        uci = igra.v_uci(int(from_sq[0]), int(from_sq[1]), int(to_sq[0]), int(to_sq[1]))
        poteza = igra.plosca.gen_pot_uci(uci)
        if igra.plosca.je_poteza_legalna(poteza):
            if  poteza.je_promocija():
                promotion_w = True if igra.plosca.barva else False
                promotion_b = True if not igra.plosca.barva else False
                prom_uci = uci
            else:
                igra.izvedi_potezo(poteza)
    is_start_sq = not is_start_sq
    bottle.redirect("/")


@bottle.post("/new_game")
def new_game():
    global is_start_sq, veljavna_poteza
    is_start_sq = True
    from_sq = "00"
    to_sq = "00"
    igra.new_game()
    bottle.redirect("/")


@bottle.post("/promotion")
def promotion():
    global prom_uci, promotion_b, promotion_w
    promotion_b = False
    promotion_w = False
    fig = bottle.request.forms.get("prom_fig")
    uci = prom_uci + fig
    poteza = igra.plosca.gen_pot_uci(uci)
    igra.izvedi_potezo(poteza)
    bottle.redirect("/")


@bottle.route("/static/<filename>")
def server_static(filename):
    return bottle.static_file(filename, root="./res")


bottle.run(host='localhost', port=8080, debug=True, reloader=True)