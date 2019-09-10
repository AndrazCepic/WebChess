import bottle
from engine.igra import Igra

igra = Igra()
new_board_input = True
click_coord = "00"

@bottle.route("/")
def index():
    return bottle.template("index", igra=igra, klik=click_coord)

@bottle.post("/board_input")
def board_input():
    global click_coord
    click_coord = bottle.request.forms.get("click")
    bottle.redirect("/")

@bottle.route("/static/<filename>")
def server_static(filename):
    return bottle.static_file(filename, root="./res")

bottle.run(host='localhost', port=8080, debug=True, reloader=True)