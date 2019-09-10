from bottle import route, run, template
from engine.igra import Igra

# TEST
stran = '<!DOCTYPE html><h1 style="">HELLO WORLD</h1>'
igra = Igra()

@route('/')
def index():
    return template("index")

run(host='localhost', port=8080, debug=True, reloader=True)