import bottle
from engine.igra import Igra

igra = Igra()
is_start_sq = True
veljavna_poteza = True
from_sq = "00"
to_sq = "00"

@bottle.route("/")
def index():
    return bottle.template("index", igra=igra, vel_pot = veljavna_poteza)

@bottle.post("/board_input")
def board_input():
    global from_sq, to_sq, is_start_sq, veljavna_poteza, igra
    if is_start_sq:
        from_sq = bottle.request.forms.get("click")
    else:
        to_sq = bottle.request.forms.get("click")
        uci = igra.v_uci(from_sq, to_sq)
        veljavna_poteza = igra.izvedi_potezo_uci(uci)
    is_start_sq = not is_start_sq
    bottle.redirect("/")

@bottle.route("/static/<filename>")
def server_static(filename):
    return bottle.static_file(filename, root="./res")

bottle.run(host='localhost', port=8080, debug=True, reloader=True)