# Librerie server
from flask import Flask
from flask import request
# Importo classe Api
from api import Api
# Conversione Stringhe -> Dizionari
import ast

index = Flask(__name__)
index.debug = True
api = Api()
link = '<img src="https://goo.gl/dmr6pW">'

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

@index.route('/get_token', methods=['POST'])
def do_login():
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


if __name__ == "__main__":
    index.run()