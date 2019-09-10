from bottle import route, run
from engine.igra import Igra

# TEST
stran = '<!DOCTYPE html><h1 style="">HELLO WORLD</h1>'

igra = Igra()

@route('/hello')
def hello():
    return stran

run(host='localhost', port=8080, debug=True)