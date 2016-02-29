# Librerie server
from flask import Flask
from flask import request
from flask import render_template
# Importo classe Api
from api import Api
# Conversione Stringhe -> Dizionari
import ast

index = Flask(__name__)
index.debug = True
api = Api()
link = '<img src="https://goo.gl/dmr6pW">'
error = '<img src="http://goo.gl/5UL9yj">'

@index.route("/")
def hello():
    return 'Welcome to TollaServer 0.1'

@index.route("/Tolla")
def tolla():
    return link

@index.route("/ping")
def ping():
    return True

@index.route("/testbg")
def testbg():
    return api.test()

@index.route('/login/<token>', methods=['POST'])
def do_login(token):
    dict_login = ast.literal_eval(request.form['dict_login'])
    usr = dict_login['username']
    psw = dict_login['password']
    if usr and psw:
        response = api.do_login(usr, psw)
        if response:
            return response
        return 0

@index.route('/login', methods=['POST'])
def do_login_token():
    token = request.form['token']
    if token:
        return api.do_login_token(token)
"""
Legenda:
/
/agenda : bad_ass_function
"""

@index.route('/agenda/<token>/<id_proj>', methods=['GET'])
def agenda (token, id_proj):
    return api.badass_function(token, id_proj)

@index.route('/activity/<id_att>')
def get_activity(id_att):
    return api.get_activity(id_att)


@index.errorhandler(404)
def page_not_found(app):
    return error, 404

if __name__ == "__main__":
    index.run()
