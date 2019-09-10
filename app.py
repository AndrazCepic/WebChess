import bottle
from engine.igra import Igra

igra = Igra()
is_start_sq = True
veljavna_poteza = True
from_sq = "00"
to_sq = "00"


# Debug
debug_str = ""


@bottle.route("/")
def index():
    return bottle.template("index", igra=igra, vel_pot=veljavna_poteza, debug_str=debug_str)


@bottle.post("/board_input")
def board_input():
    global from_sq, to_sq, is_start_sq, veljavna_poteza, debug_str
    sq = bottle.request.forms.get("click")
    if is_start_sq:
        from_sq = sq
    else:
        to_sq = sq
        uci = igra.v_uci(int(from_sq[0]), int(from_sq[1]), int(to_sq[0]), int(to_sq[1]))
        veljavna_poteza = igra.izvedi_potezo_uci(uci)

    is_start_sq = not is_start_sq
    bottle.redirect("/")


@bottle.post("/new_game")
def new_game():
    global is_start_sq, veljavna_poteza
    veljavna_poteza = True
    igra.new_game()
    bottle.redirect("/")


@bottle.route("/static/<filename>")
def server_static(filename):
    return bottle.static_file(filename, root="./res")


bottle.run(host='localhost', port=8080, debug=True, reloader=True)