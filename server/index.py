# Librerie server
from flask import Flask
from flask import request
# Importo classe Api
from api import Api

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

@index.route('/login', methods=['POST'])
def do_login():
    usr = request.form['username']
    psw = request.form['password']
    if usr and psw:
        api.do_login(usr, psw)

@index.route('/login', methods=['POST'])
def do_login_token():
    token = request.form['token']
    if token:
        return api.do_login_token(token)


if __name__ == "__main__":
    index.run()