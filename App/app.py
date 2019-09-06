from bottle import route, run
# TEST
stran = '<!DOCTYPE html><h1 style="">HELLO WORLD</h1>'

@route('/hello')
def hello():
    return stran

run(host='localhost', port=8080, debug=True)